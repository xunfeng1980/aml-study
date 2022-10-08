using CSV,DataFrames,HTTP

http_response = HTTP.get("https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv")

csv_reader = CSV.File(http_response.body)
println(typeof(csv_reader))
println(csv_reader)
