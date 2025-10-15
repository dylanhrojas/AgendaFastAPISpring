package com.example.agenda.repositories;

import com.example.agenda.models.Persona;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PersonaRepository extends JpaRepository<Persona, Integer> {

    Persona findByEmail(String email);

    boolean existsByEmail(String email);
}
