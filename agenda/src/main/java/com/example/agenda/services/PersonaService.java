package com.example.agenda.services;

import com.example.agenda.models.Persona;
import com.example.agenda.repositories.PersonaRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PersonaService {

    @Autowired
    private PersonaRepository personaRepository;

    @Autowired
    private FastAPIClient fastAPIClient;

    // Inyección de dependencias por constructor
    public PersonaService(PersonaRepository personaRepository, FastAPIClient fastAPIClient) {
        this.personaRepository = personaRepository;
        this.fastAPIClient = fastAPIClient;
    }

    // Crear o actualizar persona
    public Persona guardarPersona(Persona persona) {
        boolean esNuevo = (persona.getId() == null);

        // Guardar en base de datos local
        Persona personaGuardada = personaRepository.save(persona);

        // Enviar a FastAPI solo si es nuevo
        // (No intentamos actualizar porque los IDs no coinciden entre bases de datos)
        if (esNuevo) {
            try {
                fastAPIClient.crearPersona(personaGuardada);
            } catch (Exception e) {
                System.err.println("Error al sincronizar con FastAPI: " + e.getMessage());
            }
        }

        return personaGuardada;
    }

    // Obtener todos las personas
    public List<Persona> obtenerTodos() {
        return personaRepository.findAll();
    }

    // Buscar persona por id
    public Optional<Persona> obtenerPorId(Integer id) {
        return personaRepository.findById(id);
    }

    // Buscar persona por email
    public Optional<Persona> obtenerPorEmail(String email) {
        return Optional.ofNullable(personaRepository.findByEmail(email));
    }

    // Eliminar persona por id
    public void eliminarPersona(Integer id) {
        personaRepository.deleteById(id);

        // Eliminar en FastAPI
        try {
            fastAPIClient.eliminarPersona(id);
        } catch (Exception e) {
            System.err.println("Error al sincronizar eliminación con FastAPI: " + e.getMessage());
        }
    }

    // Verificar si existe un email
    public boolean existeEmail(String email) {
        return personaRepository.existsByEmail(email);
    }
}
