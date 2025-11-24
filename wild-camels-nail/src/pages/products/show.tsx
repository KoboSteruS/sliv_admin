/**
 * Страница просмотра заявки
 */
import { useShow } from "@refinedev/core";
import { ShowView } from "@/components/refine-ui/views/show-view";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export const ProductShow = () => {
  const { queryResult } = useShow();
  const { data, isLoading } = queryResult;

  const record = data?.data;

  if (isLoading) {
    return <div>Загрузка...</div>;
  }

  if (!record) {
    return <div>Заявка не найдена</div>;
  }

  return (
    <ShowView>
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Основная информация</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">URL источника</label>
              <p className="text-lg font-semibold">
                <a
                  href={record.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {record.source_url}
                </a>
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Цена</label>
              <p className="text-lg font-semibold">
                {new Intl.NumberFormat("ru-RU", {
                  style: "currency",
                  currency: "RUB",
                }).format(Number(record.price_rub))}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Описание</label>
              <p className="text-base">{record.description || "-"}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Дополнительная информация</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Статус</label>
                <div className="mt-1">
                  {record.status ? (
                    <Badge variant="outline">{record.status.name}</Badge>
                  ) : (
                    "-"
                  )}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Категория</label>
                <p className="text-base">{record.category?.name || "-"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Страна происхождения</label>
                <p className="text-base">{record.country_of_origin || "-"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Цвет</label>
                <p className="text-base">{record.color || "-"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Состав</label>
                <p className="text-base">{record.composition || "-"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Размерный ряд</label>
                <p className="text-base">{record.size_range || "-"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Активна</label>
                <p className="text-base">
                  <Badge variant={record.is_active ? "default" : "secondary"}>
                    {record.is_active ? "Да" : "Нет"}
                  </Badge>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Метаданные</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Поставщик</label>
                <p className="text-base">
                  {record.supplier
                    ? record.supplier.custom_name ||
                      record.supplier.first_name ||
                      record.supplier.username ||
                      `ID: ${record.supplier.id}`
                    : "-"}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Дата создания</label>
                <p className="text-base">
                  {record.created_at
                    ? new Date(record.created_at).toLocaleString("ru-RU")
                    : "-"}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Дата обновления</label>
                <p className="text-base">
                  {record.updated_at
                    ? new Date(record.updated_at).toLocaleString("ru-RU")
                    : "-"}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </ShowView>
  );
};

