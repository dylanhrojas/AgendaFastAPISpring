package com.example.agenda.controllers;

import com.example.agenda.models.Persona;
import com.example.agenda.services.PersonaService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/personas")
public class PersonaController {

    @Autowired
    private PersonaService personaService;

    // Crear persona
    @PostMapping
    public ResponseEntity<Persona> crearPersona(@RequestBody Persona persona) {
        if (personaService.existeEmail(persona.getEmail())) {
            return ResponseEntity.badRequest().build(); // Email ya registrado
        }
        Persona nuevaPersona = personaService.guardarPersona(persona);
        return ResponseEntity.ok(nuevaPersona);
    }

    // Obtener todas las personas
    @GetMapping
    public ResponseEntity<List<Persona>> obtenerTodos() {
        return ResponseEntity.ok(personaService.obtenerTodos());
    }

    // Obtener persona por ID
    @GetMapping("/{id}")
    public ResponseEntity<Persona> obtenerPorId(@PathVariable Integer id) {
        return personaService.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Actualizar persona por ID
    @PutMapping("/{id}")
    public ResponseEntity<Persona> actualizarPersona(@PathVariable Integer id, @RequestBody Persona persona) {
        return personaService.obtenerPorId(id)
                .map(p -> {
                    p.setNombre(persona.getNombre());
                    p.setApellido(persona.getApellido());
                    p.setEmail(persona.getEmail());
                    p.setTelefono(persona.getTelefono());
                    p.setDireccion(persona.getDireccion());
                    return ResponseEntity.ok(personaService.guardarPersona(p));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // Eliminar persona por ID
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarPersona(@PathVariable Integer id) {
        if (personaService.obtenerPorId(id).isPresent()) {
            personaService.eliminarPersona(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}
