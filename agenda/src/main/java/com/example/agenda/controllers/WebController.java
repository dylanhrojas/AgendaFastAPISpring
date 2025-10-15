package com.example.agenda.controllers;

import com.example.agenda.models.Persona;
import com.example.agenda.services.PersonaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/")
public class WebController {

    @Autowired
    private PersonaService personaService;

    // Página principal - Lista todas las personas
    @GetMapping
    public String index(Model model) {
        model.addAttribute("personas", personaService.obtenerTodos());
        return "index";
    }

    // Mostrar formulario para crear nueva persona
    @GetMapping("/nuevo")
    public String mostrarFormularioNuevo(Model model) {
        model.addAttribute("persona", new Persona());
        model.addAttribute("accion", "Crear");
        return "formulario";
    }

    // Procesar creación de nueva persona
    @PostMapping("/guardar")
    public String guardarPersona(@ModelAttribute Persona persona, RedirectAttributes redirectAttributes) {
        try {
            if (persona.getId() == null && personaService.existeEmail(persona.getEmail())) {
                redirectAttributes.addFlashAttribute("error", "El email ya está registrado");
                return "redirect:/nuevo";
            }
            personaService.guardarPersona(persona);
            redirectAttributes.addFlashAttribute("mensaje", "Persona guardada exitosamente");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "Error al guardar: " + e.getMessage());
        }
        return "redirect:/";
    }

    // Mostrar formulario para editar persona
    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditar(@PathVariable Integer id, Model model, RedirectAttributes redirectAttributes) {
        return personaService.obtenerPorId(id)
                .map(persona -> {
                    model.addAttribute("persona", persona);
                    model.addAttribute("accion", "Editar");
                    return "formulario";
                })
                .orElseGet(() -> {
                    redirectAttributes.addFlashAttribute("error", "Persona no encontrada");
                    return "redirect:/";
                });
    }

    // Eliminar persona
    @GetMapping("/eliminar/{id}")
    public String eliminarPersona(@PathVariable Integer id, RedirectAttributes redirectAttributes) {
        try {
            if (personaService.obtenerPorId(id).isPresent()) {
                personaService.eliminarPersona(id);
                redirectAttributes.addFlashAttribute("mensaje", "Persona eliminada exitosamente");
            } else {
                redirectAttributes.addFlashAttribute("error", "Persona no encontrada");
            }
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "Error al eliminar: " + e.getMessage());
        }
        return "redirect:/";
    }

    // Ver detalles de una persona
    @GetMapping("/ver/{id}")
    public String verPersona(@PathVariable Integer id, Model model, RedirectAttributes redirectAttributes) {
        return personaService.obtenerPorId(id)
                .map(persona -> {
                    model.addAttribute("persona", persona);
                    return "detalle";
                })
                .orElseGet(() -> {
                    redirectAttributes.addFlashAttribute("error", "Persona no encontrada");
                    return "redirect:/";
                });
    }
}
