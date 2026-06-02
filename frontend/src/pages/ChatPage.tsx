import { FormEvent, useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { fetchProvince, sendChat } from '../api/client';
import type { ChatMessage, Province } from '../types';
import './ChatPage.css';

export default function ChatPage() {
  const { code } = useParams<{ code: string }>();
  const [province, setProvince] = useState<Province | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!code) return;
    fetchProvince(code)
      .then((p) => {
        setProvince(p);
        setMessages([
          {
            role: 'assistant',
            content: `您好！我是${p.name}博物馆旅行助手。请告诉我您的出行偏好，我将为您推荐博物馆并规划行程。`,
          },
        ]);
      })
      .catch(() => setError('无法加载省份信息'));
  }, [code]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const submit = async (text: string) => {
    if (!code || !text.trim() || loading) return;

    const userMessage = text.trim();
    setInput('');
    setError(null);
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const res = await sendChat(code, userMessage);
      setMessages((prev) => [...prev, { role: 'assistant', content: res.reply }]);
      setSuggestions(res.suggestions ?? []);
    } catch (e) {
      const msg = e instanceof Error ? e.message : '发送失败';
      setError(msg);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `抱歉，暂时无法回答：${msg}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    submit(input);
  };

  if (!code) {
    return (
      <div className="chat-page">
        <p>无效的省份链接</p>
        <Link to="/">返回首页</Link>
      </div>
    );
  }

  return (
    <div className="chat-page">
      <header className="chat-header">
        <Link to="/" className="back-link">
          ← 返回地图
        </Link>
        <h1>{province?.name ?? '加载中…'} · 博物馆助手</h1>
      </header>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message message--${msg.role}`}>
            <div className="message-bubble">{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message--assistant">
            <div className="message-bubble typing">正在思考…</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((s) => (
            <button
              key={s}
              type="button"
              className="suggestion-chip"
              onClick={() => submit(s)}
              disabled={loading}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {error && <p className="chat-error">{error}</p>}

      <form className="chat-input-bar" onSubmit={onSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="例如：周末两天想带孩子看历史类博物馆"
          disabled={loading}
          maxLength={4000}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          发送
        </button>
      </form>
    </div>
  );
}
