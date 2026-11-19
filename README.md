# NutriMatch (CitizenTech) - API RESTful

Global Solution 2026.2 - FIAP - Domain Driven Design (Java).

Refatorado diretamente a partir do projeto base **Pokemon** trabalhado em aula, adaptado para o tema **CitizenTech - NutriMatch (EcoQuiosque)**: o feirante pesa as sobras de alimentos no totem EcoQuiosque com balanca IoT, publica um **Cabaz Surpresa** a preco simbolico (ou gratuito para ONGs verificadas), e o cidadao reserva no app e retira com um **QR Code** (ODS 2, 10 e 11).

## Stack

- Java 21 · Spring Boot 3.2.5 · Spring Web · Spring Data JPA · Bean Validation
- Banco de dados **Oracle (FIAP)** (`ojdbc11`) · Maven Wrapper (`mvnw`)
- Deploy: **Render.com** via Docker

## Estrutura (base direta do projeto Pokemon)

```
src/main/java/br/com/fiap/
├── CitizentechApplication.java
├── controller/
│   └── CabazController.java          # GET, POST, PUT e DELETE (/cabazes)
├── exception/
│   ├── ErroResponse.java             # corpo JSON padronizado de erro
│   ├── GlobalExceptionHandler.java   # @RestControllerAdvice (400, 404, 405, 409, 422, 500)
│   ├── RecursoNaoEncontradoException.java
│   └── RegraNegocioException.java
└── model/
    ├── bo/
    │   └── CabazBO.java              # regras de negocio (preco simbolico, ONG, reserva, QR)
    ├── dao/
    │   └── CabazDAO.java             # JpaRepository (tabela DDDJ_CABAZES)
    ├── dto/
    │   └── CabazDTO.java             # record + Bean Validation
    └── entity/
        └── Cabaz.java                # entidade JPA (@Table dddj_cabazes)
```

## Endpoints

| Metodo | Endpoint | Descricao |
|---|---|---|
| `GET` | `/cabazes` | Lista todos os cabazes (aceita `?status=DISPONIVEL`) |
| `GET` | `/cabazes/{codigo}` | Busca um cabaz pelo codigo |
| `POST` | `/cabazes` | Publica um cabaz pesado no EcoQuiosque |
| `PUT` | `/cabazes/{codigo}` | Atualiza um cabaz DISPONIVEL |
| `PUT` | `/cabazes/{codigo}/reservar` | Reserva o cabaz e gera o `codigoQr` |
| `PUT` | `/cabazes/retirar/{codigoQr}` | Confirma a retirada no EcoQuiosque via QR Code |
| `DELETE` | `/cabazes/{codigo}` | Exclui um cabaz (desde que nao esteja RESERVADO) |

## Como executar localmente

1. Configure as variaveis de ambiente (no IntelliJ: **Run -> Edit Configurations -> Environment variables**):
   - `DB_URL=jdbc:oracle:thin:@oracle.fiap.com.br:1521:ORCL`
   - `DB_USER=<seu RM>`
   - `DB_PASSWORD=<sua senha do Oracle>`
2. Execute `CitizentechApplication` ou rode `./mvnw spring-boot:run` (Windows: `mvnw.cmd spring-boot:run`).
3. Importe `insomnia/citizentech-insomnia.json` no Insomnia e teste em `http://localhost:8080`.
4. Testes automatizados (H2 em memoria, nao acessam o Oracle): `./mvnw test`.

## Deploy no Render

1. Suba o repositorio no GitHub (`https://github.com/MuriloMendes7/cityzentech_GS.git`).
2. No **render.com**, clique em **New -> Web Service** e conecte o repositorio.
3. Deixe **Root Directory** em branco (o `Dockerfile` esta na raiz do repositorio).
4. Escolha **Docker** (usa o `Dockerfile` na raiz do projeto).
5. Em **Environment Variables**, cadastre `DB_URL`, `DB_USER` e `DB_PASSWORD`.
6. Clique em **Create Web Service** e teste `GET https://<seu-servico>.onrender.com/cabazes`.

## Documentacao (PDF)

Edite `INTEGRANTES` e `URL_DEPLOY` no topo de `docs/gerar_documentacao.py` e execute:

```bash
python docs/gerar_documentacao.py
```
