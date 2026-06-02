package com.museum.service;

import com.museum.model.Province;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ProvinceService {

    private static final List<Province> PROVINCES = List.of(
            new Province("beijing", "北京市", "110000"),
            new Province("tianjin", "天津市", "120000"),
            new Province("hebei", "河北省", "130000"),
            new Province("shanxi", "山西省", "140000"),
            new Province("neimenggu", "内蒙古自治区", "150000"),
            new Province("liaoning", "辽宁省", "210000"),
            new Province("jilin", "吉林省", "220000"),
            new Province("heilongjiang", "黑龙江省", "230000"),
            new Province("shanghai", "上海市", "310000"),
            new Province("jiangsu", "江苏省", "320000"),
            new Province("zhejiang", "浙江省", "330000"),
            new Province("anhui", "安徽省", "340000"),
            new Province("fujian", "福建省", "350000"),
            new Province("jiangxi", "江西省", "360000"),
            new Province("shandong", "山东省", "370000"),
            new Province("henan", "河南省", "410000"),
            new Province("hubei", "湖北省", "420000"),
            new Province("hunan", "湖南省", "430000"),
            new Province("guangdong", "广东省", "440000"),
            new Province("guangxi", "广西壮族自治区", "450000"),
            new Province("hainan", "海南省", "460000"),
            new Province("chongqing", "重庆市", "500000"),
            new Province("sichuan", "四川省", "510000"),
            new Province("guizhou", "贵州省", "520000"),
            new Province("yunnan", "云南省", "530000"),
            new Province("xizang", "西藏自治区", "540000"),
            new Province("shaanxi", "陕西省", "610000"),
            new Province("gansu", "甘肃省", "620000"),
            new Province("qinghai", "青海省", "630000"),
            new Province("ningxia", "宁夏回族自治区", "640000"),
            new Province("xinjiang", "新疆维吾尔自治区", "650000"),
            new Province("hongkong", "香港特别行政区", "810000"),
            new Province("macau", "澳门特别行政区", "820000"),
            new Province("taiwan", "台湾省", "710000")
    );

    private final Map<String, Province> byCode = PROVINCES.stream()
            .collect(Collectors.toMap(Province::code, p -> p));

    private final Map<String, Province> byAdcode = PROVINCES.stream()
            .collect(Collectors.toMap(Province::adcode, p -> p));

    private final Map<String, Province> byName = PROVINCES.stream()
            .collect(Collectors.toMap(Province::name, p -> p));

    public List<Province> listAll() {
        return PROVINCES;
    }

    public Optional<Province> findByCode(String code) {
        return Optional.ofNullable(byCode.get(code));
    }

    public Optional<Province> findByAdcode(String adcode) {
        return Optional.ofNullable(byAdcode.get(adcode));
    }

    public Optional<Province> resolveByMapName(String mapRegionName) {
        if (mapRegionName == null || mapRegionName.isBlank()) {
            return Optional.empty();
        }
        String normalized = mapRegionName.trim();
        if (byName.containsKey(normalized)) {
            return Optional.of(byName.get(normalized));
        }
        for (Province province : PROVINCES) {
            String shortName = province.name()
                    .replace("省", "")
                    .replace("市", "")
                    .replace("自治区", "")
                    .replace("壮族", "")
                    .replace("回族", "")
                    .replace("维吾尔", "")
                    .replace("特别行政区", "");
            if (normalized.contains(shortName) || shortName.contains(normalized)) {
                return Optional.of(province);
            }
        }
        return Optional.empty();
    }
}
