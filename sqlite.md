# SQLite Music

## Questions

2.1. The definition of a foreign key is a field in one table that refers to the PRIMARY KEY in another table. This is the case for ArtistId in Album because it references the PRIMARY KEY found in the table Artists, thus it is a foreign key.

2.2. The Artist table does not have a column called AlbumId because of the nature of artists and albums. There can be one or more albums per artist, so it would not make sense to have an AlbumId column because albums are not unique to artists. For example, how would we deal with the (very real) case of the artist having multiple albums? Would we put the first album? The most recent album?

2.3. If we use an integer like CustomerId, the user can then change their email address without messing up the table. According to the microsoft website, in order to change a users primary key, we would have to copy all the values, change the one value, delete the primary key constraint and then re-create it with the new values.
In all, the process for changing the email associated with the account is much simpler if it is not the primary key.

2.4. SELECT SUM(Total) FROM Invoice

2.5. SELECT Name FROM Invoice JOIN InvoiceLine JOIN Track ON Invoice.InvoiceId = InvoiceLine.InvoiceId AND InvoiceLine.TrackId = Track.TrackId WHERE CustomerId = 50

2.6. Create a new table called Composer with a unique primary key called ComposerId and a corresponding value field called ComposerName for the composer.
Then in Track store ComposerId as a foreign key rather than Composer, so that the duplicate values will be replaced with the same ComposerId and there will not be duplicate text as both will refer to the same row in Composer that will contain the text that was once duplicate as entry ComposerName.

## Debrief

a. The review slides example of the JOIN keyword as well as the definition of foreign key: https://www.w3schools.com/sql/sql_foreignkey.asp

b. 20 minutes
