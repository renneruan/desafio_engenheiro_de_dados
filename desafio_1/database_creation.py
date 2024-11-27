import mysql.connector

# import sqlite3

# Caso não possua mysql.connector necessário rodar !pip install mysql-connector-python

# conn = sqlite3.connect("cb_database.db")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
)

cursor = conn.cursor()

# Criando Schema em banco de dados MySQL
cursor.execute(f"CREATE DATABASE desafio_cb_renne_oliveira")
cursor.execute(f"USE desafio_cb_renne_oliveira")

# A tabela menu item precisa ser criada anterior a tabela detail_lines
# tendo em vista que a mesma possui uma chave estrangeira para esta.
sql_create_menu_items_table = """
CREATE TABLE menu_items (
    miNum INTEGER PRIMARY KEY,
    modFlag BOOLEAN,
    inclTax DECIMAL(10, 6),
    activeTaxes TEXT,
    prcLvl INTEGER
);
"""

# Assim como a anterior, a tabela guest_check também precisa ser criada
# a tabela detail_lines, devido a chave estrangeira
sql_create_guest_check_table = """
CREATE TABLE guest_check (
    guestCheckId INTEGER PRIMARY KEY,
    chkNum INTEGER,
    opnBusDt DATE,
    opnUTC TIMESTAMP,
    opnLcl TIMESTAMP,
    clsdBusDt DATE,
    clsdUTC TIMESTAMP,
    clsdLcl TIMESTAMP,
    lastTransUTC TIMESTAMP,
    lastTransLcl TIMESTAMP,
    lastUpdatedUTC TIMESTAMP,
    lastUpdatedLcl TIMESTAMP,
    clsdFlag BOOLEAN,
    gstCnt INTEGER,
    subTtl DECIMAL(10, 2),
    nonTxblSlsTtl DECIMAL(10, 2),
    chkTtl DECIMAL(10, 2),
    dscTtl DECIMAL(10, 2),
    payTtl DECIMAL(10, 2),
    balDueTtl DECIMAL(10, 2),
    rvcNum INTEGER,
    otNum INTEGER,
    ocNum INTEGER,
    tblNum INTEGER,
    tblName TEXT,
    empNum INTEGER,
    numSrvcRd INTEGER,
    numChkPrntd INTEGER
);
"""

create_discounts_table = """
    CREATE TABLE discounts (
        discountId INTEGER PRIMARY KEY NOT NULL
    )
"""

create_service_charges_table = """
    CREATE TABLE service_charges (
        serviceChargeId INTEGER PRIMARY KEY NOT NULL
    )
"""

create_tender_media_table = """
    CREATE TABLE tender_media (
        tenderMediaId INTEGER PRIMARY KEY NOT NULL
    )
"""

create_error_codes_table = """
    CREATE TABLE error_codes (
        errorCodeId INTEGER PRIMARY KEY NOT NULL
    )
"""

sql_create_detail_lines_table = """
CREATE TABLE detail_lines (
    guestCheckLineItemId INTEGER PRIMARY KEY,
    rvcNum INTEGER,
    dtlOtNum INTEGER,
    dtlOcNum INTEGER,
    lineNum INTEGER,
    dtlId INTEGER,
    detailUTC TIMESTAMP,
    detailLcl TIMESTAMP,
    lastUpdateUTC TIMESTAMP,
    lastUpdateLcl TIMESTAMP,
    busDt DATE,
    wsNum INTEGER,
    dspTtl DECIMAL(10, 2),
    dspQty INTEGER,
    aggTtl DECIMAL(10, 2),
    aggQty INTEGER,
    chkEmpId INTEGER,
    chkEmpNum INTEGER,
    svcRndNum INTEGER,
    seatNum INTEGER,
    guestCheckId INTEGER NOT NULL,
    miNum INTEGER NOT NULL,
    discountId INTEGER NOT NULL,
    serviceChargeId INTEGER NOT NULL,
    tenderMediaId INTEGER NOT NULL,
    errorCodeId INTEGER NOT NULL,
    FOREIGN KEY (discountId) REFERENCES discounts(discountId),
    FOREIGN KEY (serviceChargeId) REFERENCES service_charges(serviceChargeId),
    FOREIGN KEY (tenderMediaId) REFERENCES tender_media(tenderMediaId),
    FOREIGN KEY (errorCodeId) REFERENCES error_codes(errorCodeId),
    FOREIGN KEY (guestCheckId) REFERENCES guest_check(guestCheckId) ON DELETE RESTRICT,
    FOREIGN KEY (miNum) REFERENCES menu_items(miNum) ON DELETE RESTRICT
);
"""

# Temos a criação da tabela taxes, assumimos que ela tera uma relação N:N
# com a tabela guest_check, tendo em vista que, um pedido pode ter vários
# taxes, devido ao formato de lista, e um taxes(imposto) pode ser atrelado
# a diferentes pedidos.
sql_create_taxes_table = """
CREATE TABLE taxes (
    taxNum INTEGER PRIMARY KEY,
    txblSlsTtl DECIMAL(10, 2),
    taxCollTtl DECIMAL(10, 2),
    taxRate DECIMAL(5, 2),
    type INTEGER
);
"""

# A relação N:N é criada a partir da tabela intermediária a seguir, contendo as
# chaves estrangeiras para as tabelas necessárias.
sql_create_guest_check_taxes_table = """
CREATE TABLE guest_check_taxes (
    guestCheckId INTEGER,
    taxNum INTEGER,
    PRIMARY KEY (guestCheckId, taxNum),
    FOREIGN KEY (guestCheckId) REFERENCES guest_check(guestCheckId) ON DELETE RESTRICT,
    FOREIGN KEY (taxNum) REFERENCES taxes(taxNum) ON DELETE RESTRICT
);
"""


cursor.execute(sql_create_menu_items_table)
cursor.execute(sql_create_guest_check_table)

cursor.execute(create_discounts_table)
cursor.execute(create_service_charges_table)
cursor.execute(create_tender_media_table)
cursor.execute(create_error_codes_table)

cursor.execute(sql_create_detail_lines_table)

cursor.execute(sql_create_taxes_table)
cursor.execute(sql_create_guest_check_taxes_table)


conn.commit()
conn.close()
