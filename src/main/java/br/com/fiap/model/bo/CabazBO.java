package br.com.fiap.model.bo;

import br.com.fiap.exception.RecursoNaoEncontradoException;
import br.com.fiap.exception.RegraNegocioException;
import br.com.fiap.model.dao.CabazDAO;
import br.com.fiap.model.dto.CabazDTO;
import br.com.fiap.model.entity.Cabaz;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Set;
import java.util.UUID;

@Service
public class CabazBO {

    public static final String STATUS_DISPONIVEL = "DISPONIVEL";
    public static final String STATUS_RESERVADO = "RESERVADO";
    public static final String STATUS_RETIRADO = "RETIRADO";
    public static final double PRECO_MAXIMO_SIMBOLICO = 10.0;

    private static final Set<String> STATUS_VALIDOS = Set.of(
            STATUS_DISPONIVEL, STATUS_RESERVADO, STATUS_RETIRADO
    );

    @Autowired
    private CabazDAO cabazDAO;

    @Transactional(readOnly = true)
    public List<Cabaz> consultar(String status) {
        if (status == null || status.isBlank()) {
            return cabazDAO.findAll();
        }
        String statusNormalizado = status.trim().toUpperCase();
        if (!STATUS_VALIDOS.contains(statusNormalizado)) {
            throw new RegraNegocioException("Status invalido. Use: DISPONIVEL, RESERVADO ou RETIRADO");
        }
        return cabazDAO.findByStatus(statusNormalizado);
    }

    @Transactional(readOnly = true)
    public Cabaz consultarPorCodigo(Long codigo) {
        Cabaz cabaz = cabazDAO.findByCodigo(codigo);
        if (cabaz == null) {
            throw new RecursoNaoEncontradoException("Cabaz com codigo " + codigo + " nao encontrado");
        }
        return cabaz;
    }

    @Transactional
    public Cabaz cadastrar(CabazDTO cabazDTO) {
        validarPrecoSimbolico(cabazDTO);
        Cabaz cabaz = new Cabaz(cabazDTO);
        if (Boolean.TRUE.equals(cabazDTO.gratuitoOng())) {
            cabaz.setPreco(0.0);
        }
        cabaz.setStatus(STATUS_DISPONIVEL);
        cabaz.setCodigoQr(null);
        return cabazDAO.save(cabaz);
    }

    @Transactional
    public Cabaz atualizar(Long codigo, CabazDTO cabazDTO) {
        Cabaz cabaz = consultarPorCodigo(codigo);
        if (!STATUS_DISPONIVEL.equals(cabaz.getStatus())) {
            throw new RegraNegocioException("Somente cabazes DISPONIVEIS podem ser atualizados (status atual: "
                    + cabaz.getStatus() + ")");
        }
        validarPrecoSimbolico(cabazDTO);
        cabaz.atualizar(cabazDTO);
        if (Boolean.TRUE.equals(cabazDTO.gratuitoOng())) {
            cabaz.setPreco(0.0);
        }
        return cabazDAO.save(cabaz);
    }

    @Transactional
    public Cabaz reservar(Long codigo) {
        Cabaz cabaz = consultarPorCodigo(codigo);
        if (!STATUS_DISPONIVEL.equals(cabaz.getStatus())) {
            throw new RegraNegocioException("Cabaz nao esta disponivel para reserva (status atual: "
                    + cabaz.getStatus() + ")");
        }
        cabaz.setStatus(STATUS_RESERVADO);
        cabaz.setCodigoQr(UUID.randomUUID().toString());
        return cabazDAO.save(cabaz);
    }

    @Transactional
    public Cabaz retirar(String codigoQr) {
        Cabaz cabaz = cabazDAO.findByCodigoQr(codigoQr)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Cabaz com codigo QR " + codigoQr + " nao encontrado"));
        if (!STATUS_RESERVADO.equals(cabaz.getStatus())) {
            throw new RegraNegocioException("Somente cabazes RESERVADOS podem ser retirados (status atual: "
                    + cabaz.getStatus() + ")");
        }
        cabaz.setStatus(STATUS_RETIRADO);
        return cabazDAO.save(cabaz);
    }

    @Transactional
    public void excluir(Long codigo) {
        Cabaz cabaz = consultarPorCodigo(codigo);
        if (STATUS_RESERVADO.equals(cabaz.getStatus())) {
            throw new RegraNegocioException("Cabaz RESERVADO nao pode ser excluido");
        }
        cabazDAO.deleteById(codigo);
    }

    private void validarPrecoSimbolico(CabazDTO dto) {
        if (!Boolean.TRUE.equals(dto.gratuitoOng()) && dto.preco() > PRECO_MAXIMO_SIMBOLICO) {
            throw new RegraNegocioException("O preco do cabaz deve ser simbolico (maximo R$ 10,00)");
        }
    }
}
