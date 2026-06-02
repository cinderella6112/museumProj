/**
 * ECharts 地图区域名称 -> 系统省份 code 映射
 * DataV GeoJSON 中省级名称通常为「北京」「广东」等简称
 */
export const MAP_NAME_TO_CODE: Record<string, string> = {
  北京市: 'beijing',
  天津市: 'tianjin',
  河北省: 'hebei',
  山西省: 'shanxi',
  内蒙古自治区: 'neimenggu',
  辽宁省: 'liaoning',
  吉林省: 'jilin',
  黑龙江省: 'heilongjiang',
  上海市: 'shanghai',
  江苏省: 'jiangsu',
  浙江省: 'zhejiang',
  安徽省: 'anhui',
  福建省: 'fujian',
  江西省: 'jiangxi',
  山东省: 'shandong',
  河南省: 'henan',
  湖北省: 'hubei',
  湖南省: 'hunan',
  广东省: 'guangdong',
  广西省: 'guangxi',
  海南省: 'hainan',
  重庆市: 'chongqing',
  四川省: 'sichuan',
  贵州省: 'guizhou',
  云南省: 'yunnan',
  西藏藏族自治区: 'xizang',
  陕西省: 'shaanxi',
  甘肃省: 'gansu',
  青海省: 'qinghai',
  宁夏回族自治区: 'ningxia',
  新疆: 'xinjiang',
  香港: 'hongkong',
  澳门: 'macau',
  台湾: 'taiwan',
};

export const CHINA_GEO_URL =
  'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json';
