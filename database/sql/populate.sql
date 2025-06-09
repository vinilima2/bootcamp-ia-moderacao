BEGIN TRANSACTION;

INSERT INTO Usuario VALUES ('ce23e1cb-097d-4196-adb7-d32fe78aa642','cleber','1234','30/05/2025');
INSERT INTO Post VALUES ('f73fb552-5791-42fe-9234-f09efb1bda1e','Como abastecer sem parar para pagar','Preciso para uma viagem','30/05/2025, 10:30:20','ce23e1cb-097d-4196-adb7-d32fe78aa642',0);
INSERT INTO Resposta VALUES ('f73fb552-5791-42fe-9234-f09efb1bda1e','f73fb552-5791-42fe-9234-f09efb1bda1e','Compre uma TAG sem parar em algum estabelecimento...', 'ce23e1cb-097d-4196-adb7-d32fe78aa642', '07/06/2025 13:40:20');
INSERT INTO Tag VALUES ('cultura', '30/05/2025 14:30');

COMMIT;