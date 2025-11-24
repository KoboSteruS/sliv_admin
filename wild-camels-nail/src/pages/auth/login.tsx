/**
 * Страница авторизации - ввод токена
 */
import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

export const LoginPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Если токен уже есть в URL, сохраняем его
  const urlToken = searchParams.get("token");
  if (urlToken) {
    localStorage.setItem("auth_token", urlToken);
    navigate("/products");
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      // Проверяем токен через API
      const apiUrl = import.meta.env.VITE_API_URL || "/api/v1";
      const response = await fetch(
        `${apiUrl}/products?token=${encodeURIComponent(token)}&page=1&page_size=1`
      );

      if (response.ok) {
        // Токен валиден - сохраняем и перенаправляем
        localStorage.setItem("auth_token", token);
        navigate("/products");
      } else if (response.status === 401 || response.status === 404) {
        setError("Неверный токен. Проверьте правильность ввода.");
      } else {
        setError("Ошибка при проверке токена. Попробуйте позже.");
      }
    } catch (err) {
      setError("Ошибка подключения к серверу. Проверьте, что бэкенд запущен.");
      console.error("Ошибка авторизации:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Авторизация</CardTitle>
          <CardDescription>
            Введите токен для доступа к админ-панели
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="token">Токен</Label>
              <Input
                id="token"
                type="text"
                placeholder="Введите токен"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                required
                disabled={isLoading}
                className="font-mono text-sm"
              />
              <p className="text-xs text-muted-foreground">
                Токен можно получить у администратора
              </p>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Проверка..." : "Войти"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

