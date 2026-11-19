package br.com.fiap.model.entity;

import br.com.fiap.model.dto.CabazDTO;
import jakarta.persistence.*;

import java.time.LocalDate;

@Entity(name = "Cabaz")
@Table(name = "dddj_cabazes")
public class Cabaz {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long codigo;

    @Column(nullable = false, length = 120)
    private String titulo;

    @Column(nullable = false, length = 60)
    private String categoria;

    @Column(nullable = false)
    private Double pesoKg;

    @Column(nullable = false)
    private Double preco;

    @Column(nullable = false, length = 120)
    private String quiosque;

    @Column(nullable = false, length = 120)
    private String feirante;

    @Column(nullable = false)
    private Boolean gratuitoOng;

    @Column(nullable = false, length = 20)
    private String status;

    @Column(unique = true, length = 36)
    private String codigoQr;

    @Column(nullable = false)
    private LocalDate dataPublicacao;

    private String urlImagem;

    public Cabaz() {
    }

    public Cabaz(CabazDTO cabazDTO) {
        atualizar(cabazDTO);
    }

    public void atualizar(CabazDTO cabazDTO) {
        this.titulo = cabazDTO.titulo();
        this.categoria = cabazDTO.categoria();
        this.pesoKg = cabazDTO.pesoKg();
        this.preco = cabazDTO.preco();
        this.quiosque = cabazDTO.quiosque();
        this.feirante = cabazDTO.feirante();
        this.gratuitoOng = cabazDTO.gratuitoOng();
        this.dataPublicacao = cabazDTO.dataPublicacao();
        this.urlImagem = cabazDTO.urlImagem();
    }

    public Long getCodigo() {
        return codigo;
    }

    public void setCodigo(Long codigo) {
        this.codigo = codigo;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public Double getPesoKg() {
        return pesoKg;
    }

    public void setPesoKg(Double pesoKg) {
        this.pesoKg = pesoKg;
    }

    public Double getPreco() {
        return preco;
    }

    public void setPreco(Double preco) {
        this.preco = preco;
    }

    public String getQuiosque() {
        return quiosque;
    }

    public void setQuiosque(String quiosque) {
        this.quiosque = quiosque;
    }

    public String getFeirante() {
        return feirante;
    }

    public void setFeirante(String feirante) {
        this.feirante = feirante;
    }

    public Boolean getGratuitoOng() {
        return gratuitoOng;
    }

    public void setGratuitoOng(Boolean gratuitoOng) {
        this.gratuitoOng = gratuitoOng;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getCodigoQr() {
        return codigoQr;
    }

    public void setCodigoQr(String codigoQr) {
        this.codigoQr = codigoQr;
    }

    public LocalDate getDataPublicacao() {
        return dataPublicacao;
    }

    public void setDataPublicacao(LocalDate dataPublicacao) {
        this.dataPublicacao = dataPublicacao;
    }

    public String getUrlImagem() {
        return urlImagem;
    }

    public void setUrlImagem(String urlImagem) {
        this.urlImagem = urlImagem;
    }
}
