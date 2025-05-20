import YearDropdown from "@/components/year-dropdown";
import MonthDropdown from "@/components/month-dropdown";
import CategoriesDropdown from "@/components/categories-dropdown";
interface SummaryFiltersProps {
    showOwnersDropdown?: boolean;
    showYear?: boolean;
    showMonth?: boolean;
    showCategories?: boolean;
    transactionType: "expense" | "income";
}

const SummaryFilters: React.FC<SummaryFiltersProps> = ({
    showYear = true,
    showMonth = true,
    showCategories = false,
    transactionType,
}) => {
    return (
        <div className="flex flex-wrap gap-2 p-4 border rounded-lg shadow-md">
            {showYear && (
                <div className="p-2">
                    <YearDropdown />
                </div>
            )}
            {showMonth && (
                <div className="p-2">
                    <MonthDropdown />
                </div>
            )}
            {showCategories && (
                <div className="p-2">
                    <CategoriesDropdown transactionType={transactionType} />
                </div>
            )}
        </div>
    );
};

export default SummaryFilters;
