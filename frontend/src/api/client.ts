import type { ChatResponse, Province } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE ?? '';

function getSessionId(): string {
  const key = 'museum-session-id';
  let id = sessionStorage.getItem(key);
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem(key, id);
  }
  return id;
}

export async function fetchProvinces(): Promise<Province[]> {
  const res = await fetch(`${API_BASE}/api/provinces`);
  if (!res.ok) throw new Error('加载省份列表失败');
  return res.json();
}

export async function fetchProvince(code: string): Promise<Province> {
  const res = await fetch(`${API_BASE}/api/provinces/${code}`);
  if (!res.ok) throw new Error('省份不存在');
  return res.json();
}

export async function sendChat(
  provinceCode: string,
  message: string,
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat/${provinceCode}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Session-Id': getSessionId(),
    },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    const problem = await res.json().catch(() => ({}));
    const detail =
      typeof problem.detail === 'string'
        ? problem.detail
        : '请求失败，请稍后重试';
    throw new Error(detail);
  }

  return res.json();
}
