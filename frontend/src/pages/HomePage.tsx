import ChinaMap from '../components/ChinaMap';
import './HomePage.css';

export default function HomePage() {
  return (
    <div className="home-page">
      <header className="home-header">
        <h1>博物馆推荐系统</h1>
        <p>点击地图上的省份，与省级博物馆智能助手对话，获取推荐与旅行规划</p>
      </header>
      <main className="map-container">
        <ChinaMap />
      </main>
      <footer className="home-footer">
        <span>前后端分离架构 · Spring Boot + Python 智能体</span>
      </footer>
    </div>
  );
}
