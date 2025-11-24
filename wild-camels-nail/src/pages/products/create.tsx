/**
 * Страница создания новой заявки
 */
import { useForm } from "@refinedev/react-hook-form";
import { useNavigate } from "react-router";
import { CreateView } from "@/components/refine-ui/views/create-view";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useList } from "@refinedev/core";

export const ProductCreate = () => {
  const navigate = useNavigate();
  
  const {
    refineCore: { onFinish },
    saveButtonProps,
    ...form
  } = useForm({
    refineCoreProps: {
      resource: "products",
    },
  });
  
  function onSubmit(values: Record<string, any>) {
    onFinish(values);
  }

  // Загружаем статусы
  const statusesResult = useList({
    resource: "statuses",
    meta: {
      entity_type: "product",
    },
  });

  // Загружаем категории
  const categoriesResult = useList({
    resource: "categories",
  });
  
  const statusesData = statusesResult?.data;
  const categoriesData = categoriesResult?.data;

  return (
    <CreateView>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="source_url"
            rules={{ required: "URL источника обязателен" }}
            render={({ field }) => (
              <FormItem>
                <FormLabel>URL источника</FormLabel>
                <FormControl>
                  <Input {...field} type="url" placeholder="https://example.com/product" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="price_rub"
              rules={{ required: "Цена обязательна", min: { value: 0, message: "Цена должна быть положительной" } }}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Цена (руб.)</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      value={field.value ?? ""}
                      onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : null)}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="category_id"
              rules={{ required: "Категория обязательна" }}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Категория</FormLabel>
                  <Select
                    onValueChange={(value) => field.onChange(value ? Number(value) : null)}
                    value={field.value ? String(field.value) : undefined}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Выберите категорию" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {categoriesData?.data?.map((category: { id: number; name: string }) => (
                        <SelectItem key={category.id} value={String(category.id)}>
                          {category.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={form.control}
            name="description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Описание</FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    placeholder="Введите описание товара"
                    rows={4}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="country_of_origin"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Страна происхождения</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Россия" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="color"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Цвет</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Чёрный" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="composition"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Состав</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="100% хлопок" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="size_range"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Размерный ряд</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="S, M, L, XL" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={form.control}
            name="status_id"
            rules={{ required: "Статус обязателен" }}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Статус</FormLabel>
                <Select
                  onValueChange={(value) => field.onChange(value ? Number(value) : null)}
                  value={field.value ? String(field.value) : undefined}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Выберите статус" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {statusesData?.data?.map((status: { id: number; name: string | null }) => (
                      <SelectItem key={status.id} value={String(status.id)}>
                        {status.name || `ID: ${status.id}`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="flex gap-2">
            <Button
              type="submit"
              {...saveButtonProps}
              disabled={form.formState.isSubmitting}
            >
              {form.formState.isSubmitting ? "Создание..." : "Создать"}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
            >
              Отмена
            </Button>
          </div>
        </form>
      </Form>
    </CreateView>
  );
};

