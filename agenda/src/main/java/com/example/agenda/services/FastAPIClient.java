package com.example.agenda.services;

import com.example.agenda.models.Persona;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class FastAPIClient {

    @Value("${fastapi.url}")
    private String fastApiUrl;

    private final RestTemplate restTemplate;

    public FastAPIClient() {
        this.restTemplate = new RestTemplate();
    }

    // Crear persona en FastAPI (envía solo datos, no ID)
    public void crearPersona(Persona persona) {
        try {
            String url = fastApiUrl + "/personas/";

            // Crear objeto con solo los datos necesarios (sin ID)
            Map<String, Object> personaData = new HashMap<>();
            personaData.put("nombre", persona.getNombre());
            personaData.put("apellido", persona.getApellido());
            personaData.put("email", persona.getEmail());
            personaData.put("telefono", persona.getTelefono());
            personaData.put("direccion", persona.getDireccion());

            restTemplate.postForEntity(url, personaData, Object.class);
            System.out.println("✓ Persona creada en FastAPI: " + persona.getEmail());
        } catch (Exception e) {
            System.err.println("✗ Error al crear persona en FastAPI: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // Actualizar persona en FastAPI (busca por email, no por ID)
    public void actualizarPersona(Integer id, Persona persona) {
        try {
            // Como los IDs no coinciden, buscamos por email y actualizamos
            String url = fastApiUrl + "/personas/" + id;

            Map<String, Object> personaData = new HashMap<>();
            personaData.put("nombre", persona.getNombre());
            personaData.put("apellido", persona.getApellido());
            personaData.put("email", persona.getEmail());
            personaData.put("telefono", persona.getTelefono());
            personaData.put("direccion", persona.getDireccion());

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(personaData);
            restTemplate.exchange(url, HttpMethod.PUT, request, Object.class);
            System.out.println("✓ Persona actualizada en FastAPI: " + persona.getEmail());
        } catch (Exception e) {
            System.err.println("✗ Error al actualizar persona en FastAPI: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // Eliminar persona en FastAPI
    public void eliminarPersona(Integer id) {
        try {
            String url = fastApiUrl + "/personas/" + id;
            restTemplate.delete(url);
            System.out.println("✓ Persona eliminada en FastAPI ID: " + id);
        } catch (Exception e) {
            System.err.println("✗ Error al eliminar persona en FastAPI: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
