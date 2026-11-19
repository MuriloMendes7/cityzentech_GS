package br.com.fiap.model.dto;

import jakarta.validation.constraints.*;

import java.time.LocalDate;

public record CabazDTO(
        @NotBlank
        @Size(max = 120)
        String titulo,
        @NotBlank
        @Size(max = 60)
        String categoria,
        @NotNull
        @Positive
        Double pesoKg,
        @NotNull
        @PositiveOrZero
        Double preco,
        @NotBlank
        @Size(max = 120)
        String quiosque,
        @NotBlank
        @Size(max = 120)
        String feirante,
        @NotNull
        Boolean gratuitoOng,
        @NotNull
        @PastOrPresent
        LocalDate dataPublicacao,
        String urlImagem
) {
}
