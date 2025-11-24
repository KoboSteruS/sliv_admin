/**
 * Кастомный dataProvider для работы с REST API
 * Добавляет токен в query параметры каждого запроса
 */
import { DataProvider } from "@refinedev/core";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8100/api/v1";

// Логируем URL API при загрузке модуля
console.log("[DataProvider] Инициализация:", {
  API_URL,
  VITE_API_URL: import.meta.env.VITE_API_URL,
  default: "http://localhost:8100/api/v1",
});

// Логируем URL API при загрузке
console.log("[DataProvider] Инициализация с API_URL:", API_URL);

/**
 * Получает токен из localStorage или URL параметров
 */
function getToken(): string | null {
  // Сначала проверяем localStorage (после авторизации)
  const storedToken = localStorage.getItem("auth_token");
  if (storedToken) {
    return storedToken;
  }
  
  // Если нет в localStorage, проверяем URL (для прямой ссылки с токеном)
  const urlParams = new URLSearchParams(window.location.search);
  const urlToken = urlParams.get("token");
  if (urlToken) {
    // Сохраняем токен из URL в localStorage
    localStorage.setItem("auth_token", urlToken);
    return urlToken;
  }
  
  return null;
}

/**
 * Добавляет токен к URL если он есть
 */
function addTokenToUrl(url: string): string {
  const token = getToken();
  if (!token) return url;
  
  const separator = url.includes("?") ? "&" : "?";
  return `${url}${separator}token=${encodeURIComponent(token)}`;
}

/**
 * Кастомный dataProvider для REST API
 * Автоматически добавляет токен из URL к каждому запросу
 */
export const dataProvider: DataProvider = {
  
  getList: async ({ resource, pagination, filters, sorters, meta }) => {
    console.log(`[DataProvider] getList вызван для ресурса: ${resource}`, {
      resource,
      pagination,
      filters,
      sorters,
      meta,
      API_URL,
    });
    
    const url = `${API_URL}/${resource}`;
    const urlWithToken = addTokenToUrl(url);
    
    // Строим query параметры для пагинации
    const params = new URLSearchParams();
    
    // Добавляем параметры пагинации только если пагинация включена
    if (pagination && pagination.mode !== "off") {
      const currentPage = (pagination as any).current || (pagination as any).page || 1;
      const pageSize = (pagination as any).pageSize || (pagination as any).perPage || 10;
      params.append("page", String(currentPage));
      params.append("page_size", String(pageSize));
    }
    
    // Добавляем фильтры
    if (filters) {
      filters.forEach((filter: any) => {
        if (filter && typeof filter === "object" && "field" in filter && filter.field && filter.value !== undefined) {
          params.append(filter.field, String(filter.value));
        }
      });
    }
    
    // Добавляем поиск если есть
    if (meta?.search) {
      params.append("search", meta.search);
    }
    
    // Добавляем дополнительные параметры из meta (исключаем служебные поля)
    if (meta) {
      Object.entries(meta).forEach(([key, value]) => {
        // Исключаем служебные поля Refine и React Query
        if (
          key !== "search" && 
          key !== "queryKey" && 
          key !== "signal" &&
          value !== undefined &&
          typeof value !== "object" // Игнорируем объекты (signal, queryKey)
        ) {
          params.append(key, String(value));
        }
      });
    }
    
    // Добавляем параметры к URL правильно
    let finalUrl = urlWithToken;
    const queryString = params.toString();
    
    if (queryString) {
      // Проверяем, есть ли уже query параметры в URL
      const hasQuery = urlWithToken.includes('?');
      const separator = hasQuery ? '&' : '?';
      finalUrl = `${urlWithToken}${separator}${queryString}`;
    }
    
    // Отладочная информация
    console.log(`[DataProvider] Final URL для ${resource}:`, finalUrl);
    
    // Отладочная информация
    console.log(`[DataProvider] GET ${resource}:`, {
      url: finalUrl,
      API_URL,
      pagination,
      filters,
      meta,
    });
    
    // Увеличиваем таймаут для медленных соединений
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 секунд
    
    let response;
    try {
      response = await fetch(finalUrl, {
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      clearTimeout(timeoutId);
    } catch (error: any) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        console.error(`[DataProvider] Timeout для ${resource} после 60 секунд`);
        throw new Error(`Request timeout для ${resource}`);
      }
      throw error;
    }
    
    console.log(`[DataProvider] Response ${resource}:`, {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      headers: Object.fromEntries(response.headers.entries()),
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[DataProvider] Error ${resource}:`, errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log(`[DataProvider] Response data ${resource}:`, data);
    
    // Преобразуем ответ API в формат Refine
    // Refine ожидает формат: { data: [...], total: number }
    let result;
    
    // Если ответ - массив (для statuses, categories), оборачиваем в формат Refine
    if (Array.isArray(data)) {
      result = {
        data: data,
        total: data.length,
      };
    } 
    // Если ответ - объект с полями data и total (для products)
    else if (data.data !== undefined) {
      result = {
        data: Array.isArray(data.data) ? data.data : [],
        total: typeof data.total === "number" ? data.total : (Array.isArray(data.data) ? data.data.length : 0),
      };
    }
    // Иначе возвращаем пустой массив
    else {
      result = {
        data: [],
        total: 0,
      };
    }
    
    // Отладочная информация
    console.log(`[DataProvider] getList ${resource}:`, {
      url: finalUrl,
      responseData: data,
      result,
    });
    
    return result;
  },
  
  getOne: async ({ resource, id, meta: _meta }) => {
    const url = `${API_URL}/${resource}/${id}`;
    const urlWithToken = addTokenToUrl(url);
    
    const response = await fetch(urlWithToken);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      data,
    };
  },
  
  create: async ({ resource, variables, meta: _meta }) => {
    const token = getToken();
    const url = token 
      ? `${API_URL}/${resource}?token=${encodeURIComponent(token)}`
      : `${API_URL}/${resource}`;
    
    console.log(`[DataProvider] create ${resource}:`, {
      url,
      variables,
    });
    
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(variables),
    });
    
    console.log(`[DataProvider] create ${resource} response:`, {
      status: response.status,
      ok: response.ok,
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Ошибка создания" }));
      console.error(`[DataProvider] create ${resource} error:`, error);
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      data,
    };
  },
  
  update: async ({ resource, id, variables, meta: _meta }) => {
    const token = getToken();
    const url = token 
      ? `${API_URL}/${resource}/${id}?token=${encodeURIComponent(token)}`
      : `${API_URL}/${resource}/${id}`;
    
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(variables),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Ошибка обновления" }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      data,
    };
  },
  
  deleteOne: async ({ resource, id, meta: _meta }) => {
    const token = getToken();
    const url = token 
      ? `${API_URL}/${resource}/${id}?token=${encodeURIComponent(token)}`
      : `${API_URL}/${resource}/${id}`;
    
    const response = await fetch(url, {
      method: "DELETE",
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Ошибка удаления" }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    return {
      data: { id } as any,
    };
  },
  
  getApiUrl: () => API_URL,
  
  // Дополнительные методы для полной совместимости
  getMany: async ({ resource, ids, meta: _meta }) => {
    const token = getToken();
    const promises = ids.map((id) => {
      const url = token 
        ? `${API_URL}/${resource}/${id}?token=${encodeURIComponent(token)}`
        : `${API_URL}/${resource}/${id}`;
      return fetch(url).then((res) => res.json());
    });
    
    const results = await Promise.all(promises);
    return {
      data: results,
    };
  },
  
  createMany: async ({ resource, variables, meta: _meta }) => {
    const token = getToken();
    const url = token 
      ? `${API_URL}/${resource}?token=${encodeURIComponent(token)}`
      : `${API_URL}/${resource}`;
    
    const promises = variables.map((vars) =>
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(vars),
      }).then((res) => res.json())
    );
    
    const results = await Promise.all(promises);
    return {
      data: results,
    };
  },
  
  updateMany: async ({ resource, ids, variables, meta: _meta }) => {
    const token = getToken();
    const promises = ids.map((id) => {
      const url = token 
        ? `${API_URL}/${resource}/${id}?token=${encodeURIComponent(token)}`
        : `${API_URL}/${resource}/${id}`;
      return fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      }).then((res) => res.json());
    });
    
    const results = await Promise.all(promises);
    return {
      data: results,
    };
  },
  
  deleteMany: async ({ resource, ids, meta: _meta }) => {
    const token = getToken();
    const promises = ids.map((id) => {
      const url = token 
        ? `${API_URL}/${resource}/${id}?token=${encodeURIComponent(token)}`
        : `${API_URL}/${resource}/${id}`;
      return fetch(url, {
        method: "DELETE",
      });
    });
    
    await Promise.all(promises);
    return {
      data: ids.map((id) => ({ id })) as any[],
    };
  },
  
  custom: async ({ url, method, payload, headers, meta: _meta }) => {
    const token = getToken();
    const finalUrl = addTokenToUrl(url.startsWith("http") ? url : `${API_URL}${url}`);
    
    const response = await fetch(finalUrl, {
      method: method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      body: payload ? JSON.stringify(payload) : undefined,
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Ошибка запроса" }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return {
      data,
    };
  },
};

