import SummaryFilters from "@/components/summary-filters";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ChartLinesPerson from "@/components/chart-lines-persons";
import ChartBarShops from "@/components/chart-bar-shops";
import ChartPieCategories from "@/components/chart-pie-category";

const Charts = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
            {/* Filtry z responsywnym paddingiem */}
            <div className="mb-3">
                <SummaryFilters
                    showCategories={true}
                    transactionType="expense"
                />
            </div>

            {/* Na małych ekranach jedna kolumna, od md dwóch, od lg trzech */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Tabs defaultValue="line" className="col-span-full">
                    <TabsList>
                        <TabsTrigger value="line">Bilans</TabsTrigger>
                        <TabsTrigger value="barShops">Sklepy</TabsTrigger>
                        <TabsTrigger value="pieCategories">
                            Kategorie
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="line">
                        <div className="w-full h-64 sm:h-80 md:h-96">
                            <ChartLinesPerson />
                        </div>
                    </TabsContent>
                    <TabsContent value="barShops">
                        <div className="w-full h-64 sm:h-80 md:h-96">
                            <ChartBarShops />
                        </div>
                    </TabsContent>
                    <TabsContent value="pieCategories">
                        <div className="w-full h-64 sm:h-80 md:h-96">
                            <ChartPieCategories />
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
};

export default Charts;

