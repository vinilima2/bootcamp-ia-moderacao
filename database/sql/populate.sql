BEGIN TRANSACTION;

INSERT INTO Usuario VALUES ('ce23e1cb-097d-4196-adb7-d32fe78aa642','cleber','1234','30/05/2025');
INSERT INTO Post VALUES ('f73fb552-5791-42fe-9234-f09efb1bda1e','Como ter internet de graça','Preciso para amanhã','30/05/2025','ce23e1cb-097d-4196-adb7-d32fe78aa642',0);
INSERT INTO Resposta VALUES ('f73fb552-5791-42fe-9234-f09efb1bda1e','f73fb552-5791-42fe-9234-f09efb1bda1e','Não tem como, todos os métodos hoje, são pagos.', 'ce23e1cb-097d-4196-adb7-d32fe78aa642', '07/06/2025 13:40');
INSERT INTO Tag VALUES ('cultura', '30/05/2025 14:30');

COMMIT;