# Vantage Points

## Questions

5.1. The advantage of CSV over JSON is that the file is more compact. In general, CSV formats are about half the size of JSON formats which is a major advantage if you are sending huge ammounts of data and bandwidth is an issue.

5.2. CSV requires that each row have the same number of columns, otherwise parsing the data would be impossible. This means that CSV limits the data that we can store if we want to store a variable number of one column that does not have a maximum while JSON does not have any such restrictions.

5.3. https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NFLX&interval=1min&apikey=NAJXWIA8D6VN6A3K

5.4. One way that the API could be improved would be to include in the "Meta Data" the "First Refreshed" as well as "Last Refreshed." This way if a user wanted to parse from the beginning of time rather than the end it would be possible without having to do needless arithmetic.

## Debrief

a. https://blog.datafiniti.co/4-reasons-you-should-use-json-instead-of-csv-2cac362f1943
http://ezinearticles.com/?CSV-vs-XML-vs-JSON---Which-is-the-Best-Response-Data-Format?&id=4073117

b. 30 minutes
