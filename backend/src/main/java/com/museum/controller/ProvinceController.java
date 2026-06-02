package com.museum.controller;

import com.museum.model.Province;
import com.museum.service.ProvinceService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/provinces")
public class ProvinceController {

    private final ProvinceService provinceService;

    public ProvinceController(ProvinceService provinceService) {
        this.provinceService = provinceService;
    }

    @GetMapping
    public List<Province> listProvinces() {
        return provinceService.listAll();
    }

    @GetMapping("/{code}")
    public Province getProvince(@PathVariable String code) {
        return provinceService.findByCode(code)
                .orElseThrow(() -> new IllegalArgumentException("未找到省份: " + code));
    }
}
