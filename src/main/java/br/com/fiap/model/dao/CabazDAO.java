package br.com.fiap.model.dao;

import br.com.fiap.model.entity.Cabaz;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CabazDAO extends JpaRepository<Cabaz, Long> {

    Cabaz findByCodigo(Long codigo);

    List<Cabaz> findByStatus(String status);

    Optional<Cabaz> findByCodigoQr(String codigoQr);
}
