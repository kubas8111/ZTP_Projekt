import { useState } from "react";
import { Receipt } from "@/types";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { ArrowRight } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

interface ReceiptPreviewDialogProps {
    receipt: Receipt;
    totalValue: string;
}

const ReceiptPreviewDialog: React.FC<ReceiptPreviewDialogProps> = ({
    receipt,
    totalValue,
}) => {
    const [isDialogOpen, setDialogOpen] = useState(false);

    return (
        <Dialog open={isDialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
                <Button variant="outline">
                    <ArrowRight className="w-4 h-4" />
                </Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Podgląd paragonu</DialogTitle>
                </DialogHeader>
                <div className="space-y-2">
                    <p>
                        <strong>Sklep:</strong> {receipt.shop}
                    </p>
                    <p>
                        <strong>Data:</strong> {receipt.payment_date}
                    </p>
                    <p>
                        <strong>Wartość:</strong> {totalValue} PLN
                    </p>
                    <div>
                        <strong className="mb-4 block">Właściciele:</strong>
                        <ScrollArea className="h-[300px]">
                            <ul className="list-disc pl-5">
                                {receipt.items.map((item) => (
                                    <li key={item.id} className="mb-2">
                                        {item.description} –{" "}
                                        {Number(item.value).toFixed(2)} zł{" "}
                                    </li>
                                ))}
                            </ul>
                        </ScrollArea>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
};

export interface ReceiptRowProps {
    receipt: Receipt;
    highlightOwners?: boolean; // opcjonalnie, nie używamy już tej wartości
    onEdit?: (id: number) => void;
}

export const ReceiptRow: React.FC<ReceiptRowProps> = ({ receipt, onEdit }) => {
    // Obliczenie całkowitej wartości paragonu
    const totalValue = receipt.items.reduce(
        (sum, item) => sum + Number(item.value),
        0
    );

    return (
        <div className="grid grid-cols-3 gap-4 items-center py-2 border-b">
            <div className="truncate font-bold col-span-2 lg:col-span-1">
                {receipt.shop}
            </div>
            <div className="truncate col-span-2 lg:col-span-1">
                {totalValue.toFixed(2)} PLN
            </div>

            <div className="flex justify-end">
                {onEdit ? (
                    <Button
                        variant="outline"
                        onClick={() => onEdit(receipt.id)}>
                        <ArrowRight className="w-4 h-4" />
                    </Button>
                ) : (
                    <ReceiptPreviewDialog
                        receipt={receipt}
                        totalValue={totalValue.toFixed(2)}
                    />
                )}
            </div>
        </div>
    );
};
