import { ZodError } from "zod";
import { AxiosError } from "axios";
import { toast } from "sonner";

type AnyError = string | Error | ZodError | AxiosError | unknown;

function toMessages(raw: AnyError): string[] {
    if (raw instanceof ZodError) {
        return raw.errors.map((issue) => issue.message);
    }

    if (raw instanceof AxiosError && raw.response) {
        return toMessages(raw.response.data);
    }

    if (typeof raw === "string") return [raw];
    if (raw instanceof Error && raw.message) return [raw.message];

    if (Array.isArray(raw)) {
        return raw.flatMap((item) => toMessages(item));
    }

    if (typeof raw === "object" && raw !== null) {
        return Object.values(raw).flatMap((v) => toMessages(v));
    }

    return ["Nieznany błąd"];
}

export function showError(err: AnyError, opts: { oneToast?: boolean } = {}) {
    const msgs = toMessages(err);

    if (opts.oneToast) {
        toast.error(msgs.join("\n"), { style: { whiteSpace: "pre-line" } });
    } else {
        msgs.forEach((m) => toast.error(m));
    }
}
