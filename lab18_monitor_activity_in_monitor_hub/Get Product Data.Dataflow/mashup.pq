[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "3fd6a85a-8c02-4d5a-9f0e-27028a843272"]}[Data]{[lakehouseId = "0b9a43aa-e391-462b-83c9-8db3f5f290ba"]}[Data];
[BindToDefaultDestination = true]
shared products = let
  Source = Csv.Document(Web.Contents("https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/products.csv"), [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"ProductID", Int64.Type}, {"ProductName", type text}, {"Category", type text}, {"ListPrice", type number}})
in
  #"Changed column type";
