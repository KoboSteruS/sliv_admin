/**
 * Страница списка статусов
 */
import { useTable } from "@refinedev/react-table";
import { createColumnHelper } from "@tanstack/react-table";
import React from "react";

import { DataTable } from "@/components/refine-ui/data-table/data-table";
import { ListView } from "@/components/refine-ui/views/list-view";
import { Badge } from "@/components/ui/badge";

type Status = {
  id: number;
  entity_type: string | null;
  code: string | null;
  name: string | null;
  color: string | null;
  order_index: number | null;
  is_final: boolean | null;
};

export const StatusList = () => {
  const columns = React.useMemo(() => {
    const columnHelper = createColumnHelper<Status>();

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
        cell: ({ getValue, row }) => {
          const name = getValue();
          const color = row.original.color;
          return (
            <Badge 
              variant="outline" 
              style={color ? { borderColor: color, color: color } : undefined}
            >
              {name || "-"}
            </Badge>
          );
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
      columnHelper.accessor("entity_type", {
        id: "entity_type",
        header: "Тип сущности",
        enableSorting: true,
      }),
      columnHelper.accessor("order_index", {
        id: "order_index",
        header: "Порядок",
        enableSorting: true,
      }),
      columnHelper.accessor("is_final", {
        id: "is_final",
        header: "Финальный",
        enableSorting: true,
        cell: ({ getValue }) => {
          const isFinal = getValue();
          return isFinal ? "Да" : "Нет";
        },
      }),
    ];
  }, []);

  const table = useTable<Status>({
    columns,
    refineCoreProps: {
      resource: "statuses",
      syncWithLocation: true,
      meta: {
        entity_type: "product",
      },
    },
  });

  return (
    <ListView>
      <DataTable table={table} />
    </ListView>
  );
};

