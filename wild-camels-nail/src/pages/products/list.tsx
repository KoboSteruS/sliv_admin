/**
 * Страница "Заявки" - список заявок (products)
 */
import { useList } from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { createColumnHelper } from "@tanstack/react-table";
import React from "react";

import { DeleteButton } from "@/components/refine-ui/buttons/delete";
import { EditButton } from "@/components/refine-ui/buttons/edit";
import { ShowButton } from "@/components/refine-ui/buttons/show";
import { DataTable } from "@/components/refine-ui/data-table/data-table";
import { ListView } from "@/components/refine-ui/views/list-view";
import { Breadcrumb } from "@/components/refine-ui/layout/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { CreateProductModal } from "@/components/create-product-modal";

type Product = {
  id: number;
  source_url: string;
  price_rub: number;
  category_id: number;
  status_id: number;
  supplier_user_id: number;
  country_of_origin: string | null;
  composition: string | null;
  size_range: string | null;
  color: string | null;
  description: string | null;
  attributes: Record<string, any> | null;
  is_active: boolean;
  approved_by: number | null;
  approved_at: string | null;
  status: { id: number; name: string | null; code: string | null } | null;
  category: { id: number; name: string | null; code: string | null } | null;
  supplier: {
    id: number;
    custom_name: string | null;
    first_name: string | null;
    username: string | null;
    email: string | null;
    role: string;
  } | null;
  created_at: string;
  updated_at: string;
};

export const ProductList = () => {
  // Загружаем статусы для фильтрации (только для продуктов)
  const statusesResult = useList({
    resource: "statuses",
    meta: {
      entity_type: "product",
    },
  });

  // Загружаем категории для фильтрации
  const categoriesResult = useList({
    resource: "categories",
  });
  
  const statuses = statusesResult?.data?.data || [];
  const categories = categoriesResult?.data?.data || [];

  const columns = React.useMemo(() => {
    const columnHelper = createColumnHelper<Product>();

    return [
      columnHelper.accessor("source_url", {
        id: "source_url",
        header: "URL источника",
        enableSorting: true,
        cell: ({ getValue }) => {
          const url = getValue();
          return (
            <div className="max-w-xs">
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline truncate block"
                title={url}
              >
                {url.length > 40 ? `${url.slice(0, 40)}...` : url}
              </a>
            </div>
          );
        },
      }),
      columnHelper.accessor("price_rub", {
        id: "price_rub",
        header: "Цена",
        enableSorting: true,
        cell: ({ getValue }) => {
          const price = getValue();
          return new Intl.NumberFormat("ru-RU", {
            style: "currency",
            currency: "RUB",
          }).format(Number(price));
        },
      }),
      columnHelper.accessor("status.name", {
        id: "status",
        header: "Статус",
        enableSorting: false,
        cell: ({ row }) => {
          const status = row.original.status;
          if (!status || !status.name) return "-";
          return (
            <Badge variant="outline">
              {status.name}
            </Badge>
          );
        },
      }),
      columnHelper.accessor("category.name", {
        id: "category",
        header: "Категория",
        enableSorting: false,
        cell: ({ row }) => {
          const category = row.original.category;
          if (!category) return "-";
          return <div>{category.name || `ID: ${category.id}`}</div>;
        },
      }),
      columnHelper.accessor("supplier", {
        id: "supplier",
        header: "Поставщик",
        enableSorting: false,
        cell: ({ row }) => {
          const supplier = row.original.supplier;
          if (!supplier) return "-";
          const name = supplier.custom_name || 
                      supplier.first_name || 
                      supplier.username || 
                      `ID: ${supplier.id}`;
          return <div>{name}</div>;
        },
      }),
      columnHelper.accessor("description", {
        id: "description",
        header: "Описание",
        enableSorting: false,
        cell: ({ getValue }) => {
          const description = getValue();
          if (!description) return "-";
          return (
            <div className="max-w-xs truncate" title={description}>
              {description.length > 50 ? `${description.slice(0, 50)}...` : description}
            </div>
          );
        },
      }),
      columnHelper.accessor("is_active", {
        id: "is_active",
        header: "Активна",
        enableSorting: true,
        cell: ({ getValue }) => {
          const isActive = getValue();
          return (
            <Badge variant={isActive ? "default" : "secondary"}>
              {isActive ? "Да" : "Нет"}
            </Badge>
          );
        },
      }),
      columnHelper.accessor("created_at", {
        id: "created_at",
        header: "Дата создания",
        enableSorting: true,
        cell: ({ getValue }) => {
          const date = getValue();
          if (!date) return "-";
          return new Date(date).toLocaleString("ru-RU", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
          });
        },
      }),
      columnHelper.display({
        id: "actions",
        header: "Действия",
        cell: ({ row }) => (
          <div className="flex gap-2">
            <EditButton recordItemId={row.original.id} size="sm" />
            <ShowButton recordItemId={row.original.id} size="sm" />
            <DeleteButton recordItemId={row.original.id} size="sm" />
          </div>
        ),
        enableSorting: false,
        size: 200,
      }),
    ];
  }, []);

  const table = useTable<Product>({
    columns,
    refineCoreProps: {
      resource: "products",
      syncWithLocation: true,
    },
  });
  
  // Отладочная информация
  React.useEffect(() => {
    console.log("=== Products Table Debug ===");
    console.log("refineCore:", table.refineCore);
    console.log("data:", table.refineCore?.queryResult?.data);
    console.log("error:", table.refineCore?.queryResult?.error);
    console.log("isLoading:", table.refineCore?.queryResult?.isLoading);
    console.log("isFetching:", table.refineCore?.queryResult?.isFetching);
    console.log("refetch:", table.refineCore?.queryResult?.refetch);
    console.log("===========================");
  }, [table.refineCore]);

  return (
    <ListView>
      <div className="flex flex-col gap-4">
        <div className="flex items-center relative gap-2">
          <div className="bg-background z-[2] pr-4">
            <Breadcrumb />
          </div>
          <Separator className="absolute left-0 right-0 z-[1]" />
        </div>
        <div className="flex justify-between gap-4 items-center">
          <h2 className="text-2xl font-bold">Заявки</h2>
          <div className="flex items-center gap-2">
            <CreateProductModal />
          </div>
        </div>
      </div>
      <DataTable table={table} />
    </ListView>
  );
};

