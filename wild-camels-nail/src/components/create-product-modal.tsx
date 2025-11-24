/**
 * Модальное окно для создания новой заявки
 */
import { useState, useEffect } from "react";
import React from "react";
import { useCreate, useInvalidate } from "@refinedev/core";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useForm } from "react-hook-form";
import { Plus } from "lucide-react";
import { toast } from "sonner";

type FormValues = {
  source_url: string;
  price_rub: number;
  category_id: number;
};

export const CreateProductModal = () => {
  const [open, setOpen] = useState(false);
  const [isPending, setIsPending] = useState(false);
  const { mutate: createProduct } = useCreate();
  const invalidate = useInvalidate();
  
  // Загружаем категории напрямую через fetch
  const [categories, setCategories] = React.useState<any[]>([]);
  const [categoriesLoading, setCategoriesLoading] = React.useState(true);
  const [categoriesError, setCategoriesError] = React.useState<Error | null>(null);
  
  React.useEffect(() => {
    const loadCategories = async () => {
      try {
        setCategoriesLoading(true);
        setCategoriesError(null);
        
        const token = localStorage.getItem("auth_token");
        const apiUrl = import.meta.env.VITE_API_URL || "/api/v1";
        const url = `${apiUrl}/categories${token ? `?token=${encodeURIComponent(token)}` : ''}`;
        
        console.log("[CreateProductModal] Загрузка категорий:", url);
        
        const response = await fetch(url, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("[CreateProductModal] Категории загружены:", data);
        
        // API возвращает массив категорий
        if (Array.isArray(data)) {
          setCategories(data);
        } else {
          setCategories([]);
        }
      } catch (error: any) {
        console.error("[CreateProductModal] Ошибка загрузки категорий:", error);
        setCategoriesError(error);
        setCategories([]);
      } finally {
        setCategoriesLoading(false);
      }
    };
    
    loadCategories();
  }, []); // Загружаем только при монтировании компонента
  
  // Отладочная информация
  React.useEffect(() => {
    console.log("[CreateProductModal] Categories Debug:", {
      categories: categories,
      categoriesLength: categories.length,
      categoriesLoading,
      categoriesError: categoriesError ? {
        message: categoriesError.message,
        stack: categoriesError.stack,
      } : null,
      firstCategory: categories[0],
    });
  }, [categories, categoriesLoading, categoriesError]);
  
  const form = useForm<FormValues>({
    defaultValues: {
      source_url: "",
      price_rub: 0,
      category_id: 0,
    },
    mode: "onChange",
  });

  const onSubmit = (values: FormValues) => {
    // Валидация
    if (!values.source_url || !values.category_id || values.price_rub <= 0) {
      toast.error("Ошибка", {
        description: "Заполните все обязательные поля",
      });
      return;
    }

    // Создаём заявку через API
    // status_id не передаём - бэкенд установит автоматически "новый"
    setIsPending(true);
    createProduct(
      {
        resource: "products",
        values: {
          source_url: values.source_url,
          price_rub: values.price_rub,
          category_id: values.category_id,
          // status_id не передаём - бэкенд установит автоматически
        },
      },
      {
        onSuccess: () => {
          toast.success("Успешно", {
            description: "Заявка создана",
          });
          // Обновляем список заявок
          invalidate({
            resource: "products",
            invalidates: ["list"],
          });
          setOpen(false);
          form.reset();
          setIsPending(false);
        },
        onError: (error: any) => {
          toast.error("Ошибка", {
            description: error?.message || "Не удалось создать заявку",
          });
          setIsPending(false);
        },
      }
    );
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Создать заявку
        </Button>
      </DialogTrigger>
      
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Создать новую заявку</DialogTitle>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="source_url"
              rules={{ required: "URL источника обязателен" }}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Ссылка на товар *</FormLabel>
                  <FormControl>
                    <Input 
                      {...field} 
                      type="url" 
                      placeholder="https://example.com/product" 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="price_rub"
                rules={{ 
                  required: "Цена обязательна", 
                  min: { value: 0.01, message: "Цена должна быть больше 0" } 
                }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Цена (руб.) *</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        type="number"
                        step="0.01"
                        min="0.01"
                        placeholder="0.00"
                        value={field.value ?? ""}
                        onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : 0)}
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
                    <FormLabel>Категория *</FormLabel>
                    <Select
                      onValueChange={(value) => field.onChange(value ? Number(value) : 0)}
                      value={field.value ? String(field.value) : undefined}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Выберите категорию" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categoriesLoading ? (
                          <SelectItem value="loading" disabled>
                            Загрузка категорий...
                          </SelectItem>
                        ) : categories.length === 0 ? (
                          <SelectItem value="empty" disabled>
                            Категории не найдены
                          </SelectItem>
                        ) : (
                          categories.map((category: any) => (
                            <SelectItem key={category.id} value={String(category.id)}>
                              {category.name || `Категория ${category.id}`}
                            </SelectItem>
                          ))
                        )}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <p className="text-xs text-muted-foreground">
              * Обязательные поля. Заявка автоматически получит статус "Новая"
            </p>

            <div className="flex justify-end gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  setOpen(false);
                  form.reset();
                }}
                disabled={isPending}
              >
                Отмена
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending ? "Создание..." : "Создать"}
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};
