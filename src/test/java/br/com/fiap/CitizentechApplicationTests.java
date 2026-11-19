package br.com.fiap;

import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class CitizentechApplicationTests {

    @Value("${local.server.port}")
    private int port;

    private final HttpClient http = HttpClient.newHttpClient();

    private static String codigoCabaz1;
    private static String codigoCabaz2;
    private static String codigoQr;

    private HttpResponse<String> call(String method, String path, String body) throws Exception {
        HttpRequest.Builder builder = HttpRequest.newBuilder(URI.create("http://localhost:" + port + path))
                .header("Content-Type", "application/json");
        builder.method(method, body == null ? HttpRequest.BodyPublishers.noBody()
                : HttpRequest.BodyPublishers.ofString(body));
        return http.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }

    private static String campo(String json, String nome) {
        Matcher m = Pattern.compile("\"" + nome + "\"\\s*:\\s*(\"([^\"]*)\"|[^,}\\s]+)").matcher(json);
        assertTrue(m.find(), "campo " + nome + " nao encontrado em " + json);
        return m.group(2) != null ? m.group(2) : m.group(1);
    }

    @Test
    @Order(1)
    void deveCadastrarCabazComumECabazGratuitoOng() throws Exception {
        var r1 = call("POST", "/cabazes", """
                {
                  "titulo": "Cabaz Surpresa de Verduras",
                  "categoria": "Hortifruti",
                  "pesoKg": 4.5,
                  "preco": 5.0,
                  "quiosque": "EcoQuiosque EQ-001 - Mercado Central",
                  "feirante": "Banca da Maria",
                  "gratuitoOng": false,
                  "dataPublicacao": "2026-11-18",
                  "urlImagem": "https://exemplo.com/cabaz-verduras.png"
                }
                """);
        assertEquals(201, r1.statusCode());
        assertEquals("DISPONIVEL", campo(r1.body(), "status"));
        assertEquals("5.0", campo(r1.body(), "preco"));
        codigoCabaz1 = campo(r1.body(), "codigo");

        // Segundo cabaz (gratuitoOng=true -> preco forcado para 0.0, e testa 2 registros com codigoQr=null)
        var r2 = call("POST", "/cabazes", """
                {
                  "titulo": "Cabaz Solidario de Frutas",
                  "categoria": "Frutas",
                  "pesoKg": 6.0,
                  "preco": 8.0,
                  "quiosque": "EcoQuiosque EQ-002 - Feira da Vila",
                  "feirante": "Barraca do Joao",
                  "gratuitoOng": true,
                  "dataPublicacao": "2026-11-18",
                  "urlImagem": ""
                }
                """);
        assertEquals(201, r2.statusCode());
        assertEquals("0.0", campo(r2.body(), "preco"));
        codigoCabaz2 = campo(r2.body(), "codigo");
    }

    @Test
    @Order(2)
    void deveTratarExcecoesDeValidacaoERegraDeNegocio() throws Exception {
        // Bean Validation -> 400
        var invalido = call("POST", "/cabazes", """
                {"titulo": "", "categoria": "", "pesoKg": -2.0, "preco": -1.0,
                 "quiosque": "", "feirante": "", "gratuitoOng": false, "dataPublicacao": "2099-01-01"}
                """);
        assertEquals(400, invalido.statusCode());
        assertTrue(invalido.body().contains("\"status\":400"));

        // Preco acima do simbolico (> 10.0) -> 422
        var caro = call("POST", "/cabazes", """
                {"titulo": "Cabaz Caro", "categoria": "Frutas", "pesoKg": 2.0, "preco": 25.0,
                 "quiosque": "EQ-001", "feirante": "Maria", "gratuitoOng": false, "dataPublicacao": "2026-11-18"}
                """);
        assertEquals(422, caro.statusCode());

        // Nao encontrado -> 404
        assertEquals(404, call("GET", "/cabazes/9999", null).statusCode());

        // Tipo invalido na URL -> 400
        assertEquals(400, call("GET", "/cabazes/abc", null).statusCode());

        // Status de filtro invalido -> 422
        assertEquals(422, call("GET", "/cabazes?status=INEXISTENTE", null).statusCode());
    }

    @Test
    @Order(3)
    void deveConsultarAtualizarReservarRetirarEExcluir() throws Exception {
        assertEquals(200, call("GET", "/cabazes", null).statusCode());
        assertEquals(200, call("GET", "/cabazes?status=DISPONIVEL", null).statusCode());
        assertEquals(200, call("GET", "/cabazes/" + codigoCabaz1, null).statusCode());

        // PUT atualizar
        var put = call("PUT", "/cabazes/" + codigoCabaz1, """
                {
                  "titulo": "Cabaz Surpresa de Verduras e Legumes",
                  "categoria": "Hortifruti",
                  "pesoKg": 5.2,
                  "preco": 6.0,
                  "quiosque": "EcoQuiosque EQ-001 - Mercado Central",
                  "feirante": "Banca da Maria",
                  "gratuitoOng": false,
                  "dataPublicacao": "2026-11-18",
                  "urlImagem": "https://exemplo.com/cabaz-atualizado.png"
                }
                """);
        assertEquals(200, put.statusCode());
        assertEquals("Cabaz Surpresa de Verduras e Legumes", campo(put.body(), "titulo"));

        // PUT reservar -> gera QR Code e muda status para RESERVADO
        var res = call("PUT", "/cabazes/" + codigoCabaz1 + "/reservar", null);
        assertEquals(200, res.statusCode());
        assertEquals("RESERVADO", campo(res.body(), "status"));
        codigoQr = campo(res.body(), "codigoQr");

        // Nao pode reservar novamente nem excluir enquanto RESERVADO -> 422
        assertEquals(422, call("PUT", "/cabazes/" + codigoCabaz1 + "/reservar", null).statusCode());
        assertEquals(422, call("DELETE", "/cabazes/" + codigoCabaz1, null).statusCode());

        // PUT retirar por QR Code -> muda status para RETIRADO
        var ret = call("PUT", "/cabazes/retirar/" + codigoQr, null);
        assertEquals(200, ret.statusCode());
        assertEquals("RETIRADO", campo(ret.body(), "status"));
        assertEquals(404, call("PUT", "/cabazes/retirar/qr-inexistente", null).statusCode());

        // DELETE -> 204
        assertEquals(204, call("DELETE", "/cabazes/" + codigoCabaz1, null).statusCode());
        assertEquals(204, call("DELETE", "/cabazes/" + codigoCabaz2, null).statusCode());
        assertEquals(404, call("GET", "/cabazes/" + codigoCabaz1, null).statusCode());
    }
}
