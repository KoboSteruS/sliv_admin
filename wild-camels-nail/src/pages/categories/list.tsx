/**
 * Страница списка категорий
 */
import { useTable } from "@refinedev/react-table";
import { createColumnHelper } from "@tanstack/react-table";
import React from "react";

import { DataTable } from "@/components/refine-ui/data-table/data-table";
import { ListView } from "@/components/refine-ui/views/list-view";

type Category = {
  id: number;
  code: string | null;
  name: string | null;
  required_fields: any[] | null;
  created_at: string | null;
};

export const CategoryList = () => {
  const columns = React.useMemo(() => {
    const columnHelper = createColumnHelper<Category>();

    return [
      columnHelper.accessor("id", {
        id: "id",
        header: "ID",
        enableSorting: true,
      }),
      columnHelper.accessor("name", {
        id: "name",
        header: "Название",
        enableSorting: true,
        cell: ({ getValue }) => {
          const name = getValue();
          return <div className="font-medium">{name || "-"}</div>;
        },
      }),
      columnHelper.accessor("code", {
        id: "code",
        header: "Код",
        enableSorting: true,
        cell: ({ getValue }) => {
          const code = getValue();
          return <code className="text-sm">{code || "-"}</code>;
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
    ];
  }, []);

  const table = useTable<Category>({
    columns,
    refineCoreProps: {
      resource: "categories",
      syncWithLocation: true,
    },
  });

  return (
    <ListView>
      <DataTable table={table} />
    </ListView>
  );
};
