import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { useNavigate } from 'react-router-dom';
import { CHINA_GEO_URL, MAP_NAME_TO_CODE } from '../data/provinceMap';

export default function ChinaMap() {
  const chartRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!chartRef.current) return;

    const chart = echarts.init(chartRef.current);
    let disposed = false;

    const loadMap = async () => {
      try {
        const res = await fetch(CHINA_GEO_URL);
        const geoJson = await res.json();
        if (disposed) return;

        echarts.registerMap('china', geoJson);
        chart.setOption({
          title: {
            text: '选择省份，开启博物馆之旅',
            left: 'center',
            top: 12,
            textStyle: { fontSize: 18, color: '#1a1a2e' },
          },
          tooltip: {
            trigger: 'item',
            formatter: (params: { name?: string }) =>
              params.name ? `点击进入 ${params.name} 智能助手` : '',
          },
          series: [
            {
              name: '中国',
              type: 'map',
              map: 'china',
              roam: true,
              scaleLimit: { min: 0.8, max: 3 },
              label: { show: true, fontSize: 10, color: '#333' },
              emphasis: {
                label: { show: true, fontSize: 12, fontWeight: 'bold' },
                itemStyle: { areaColor: '#4a90d9', borderColor: '#fff' },
              },
              itemStyle: {
                areaColor: '#dce9f5',
                borderColor: '#fff',
                borderWidth: 1,
              },
              select: {
                itemStyle: { areaColor: '#2c6fad' },
              },
            },
          ],
        });

        chart.on('click', (params: { name?: string }) => {
          const name = params.name?.trim();
          if (!name) return;
          const code = MAP_NAME_TO_CODE[name];
          if (code) {
            navigate(`/province/${code}`);
          }
        });
      } catch {
        chart.setOption({
          title: {
            text: '地图加载失败，请检查网络后刷新',
            left: 'center',
            top: 'center',
            textStyle: { color: '#c0392b' },
          },
        });
      }
    };

    loadMap();

    const onResize = () => chart.resize();
    window.addEventListener('resize', onResize);

    return () => {
      disposed = true;
      window.removeEventListener('resize', onResize);
      chart.dispose();
    };
  }, [navigate]);

  return <div ref={chartRef} className="china-map" />;
}
