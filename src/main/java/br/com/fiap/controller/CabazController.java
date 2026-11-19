package br.com.fiap.controller;

import br.com.fiap.model.bo.CabazBO;
import br.com.fiap.model.dto.CabazDTO;
import br.com.fiap.model.entity.Cabaz;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/cabazes")
public class CabazController {

    @Autowired
    private CabazBO cabazBO;

    // POST localhost:8080/cabazes
    @PostMapping
    public ResponseEntity<Cabaz> cadastrar(@RequestBody @Valid CabazDTO cabazDTO) {
        Cabaz cabaz = cabazBO.cadastrar(cabazDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(cabaz);
    }

    // GET localhost:8080/cabazes  ou  GET localhost:8080/cabazes?status=DISPONIVEL
    @GetMapping
    public ResponseEntity<List<Cabaz>> consultar(@RequestParam(required = false) String status) {
        return ResponseEntity.ok(cabazBO.consultar(status));
    }

    // GET localhost:8080/cabazes/{codigo}
    @GetMapping("/{codigo}")
    public ResponseEntity<Cabaz> consultarPorCodigo(@PathVariable Long codigo) {
        return ResponseEntity.ok(cabazBO.consultarPorCodigo(codigo));
    }

    // PUT localhost:8080/cabazes/{codigo}
    @PutMapping("/{codigo}")
    public ResponseEntity<Cabaz> atualizar(@PathVariable Long codigo,
                                           @RequestBody @Valid CabazDTO cabazDTO) {
        return ResponseEntity.ok(cabazBO.atualizar(codigo, cabazDTO));
    }

    // PUT localhost:8080/cabazes/{codigo}/reservar
    @PutMapping("/{codigo}/reservar")
    public ResponseEntity<Cabaz> reservar(@PathVariable Long codigo) {
        return ResponseEntity.ok(cabazBO.reservar(codigo));
    }

    // PUT localhost:8080/cabazes/retirar/{codigoQr}
    @PutMapping("/retirar/{codigoQr}")
    public ResponseEntity<Cabaz> retirar(@PathVariable String codigoQr) {
        return ResponseEntity.ok(cabazBO.retirar(codigoQr));
    }

    // DELETE localhost:8080/cabazes/{codigo}
    @DeleteMapping("/{codigo}")
    public ResponseEntity<Void> excluir(@PathVariable Long codigo) {
        cabazBO.excluir(codigo);
        return ResponseEntity.noContent().build();
    }
}
