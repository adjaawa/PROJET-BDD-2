from pyparsing import CaselessKeyword, delimitedList, Combine, ParseException, CharsNotIn, Each, Forward , Group , Optional , Word , OneOrMore, alphas , alphanums, nums, oneOf, ZeroOrMore, quotedString, restOfLine, Keyword

sqlComment = '--' + restOfLine

def parseCreateDatabase (request) :

    createDatabaseKeywords = ["create", "database", "if", "not", "exists",]
    [create, database, _if, _not, exists] = [ CaselessKeyword (word) for word in createDatabaseKeywords]

    createDatabaseStatement = Forward().setName("Create Database statement")

    database_name = Word (alphas, alphanums)
    table_name = Word (alphas, alphanums)

    createDatabaseStatement << ( create +
                    database +
                    Optional (_if + _not + exists) +
                    database_name.setResultsName('Database') + 
                    ';'
                )
    createDatabaseStatement.ignore(sqlComment)

    try :
        tokens = createDatabaseStatement.parseString(request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseCreateTable (request) :

    createTableKeywords = ["create", "table", "if", "not", "exists",]
    [create, table, _if, _not, exists] = [ CaselessKeyword (word) for word in createTableKeywords]

    createTableStatement = Forward().setName("Create Table statement")
    table_name = Word (alphas, alphanums)

    wth = "(" + ZeroOrMore(CharsNotIn(")")) + ")"
    field_def = OneOrMore (Word (alphas, alphanums) | wth)

    def field_act (s, loc ,tok) :
        return ('<' + tok[0] + '> ' + ' '.join(tok[1:])).replace('"','\\"')

    field_def.setParseAction (field_act)
    field_list_def = delimitedList (field_def)

    createTableStatement << ( create +
                            table + 
                            Optional (_if + _not + exists) +
                            table_name.setResultsName('Table') +
                            "(" +
                            field_list_def.setResultsName('Columns') +
                            ')' +
                            ';'
                        )

    createTableStatement.ignore(sqlComment)

    columnsDesc = []
    columns = []
    try :
        tokens = createTableStatement.parseString(request)

        for i in range (len(tokens.Columns)) :
            columnsDesc.append (tokens.Columns[i].split(" "))
        
        for a in range (len(columnsDesc)):
            for b in range (2) :
                if b % 2 == 0 :
                    columns.append (str (columnsDesc[a][b]).strip('<>'))

        tokens.Columns = columns
        return tokens

    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseSelect (request) :

    selectKeywords = ["select", "from", "where", "group by", "order by", "and", "or", "in"]
    [select, _from , where, groupby, orderby , _and, _or, _in] = [ CaselessKeyword (word) for word in selectKeywords]

    ident = Word (alphas, alphanums + "_$").setName('Identifier')
    column = (delimitedList (ident , '.', combine = True))
    columns = Group (delimitedList(column))
    table = (delimitedList (ident, '.', combine = True))
    tables = Group (delimitedList (table))
    columnVal = (nums | quotedString)

    whereCond = (column + oneOf (" = < > <= >= !=", caseless = True) + columnVal)
    whereExpr = whereCond + ZeroOrMore ((_and | _or) + whereCond)

    selectStatement = Forward().setName ("Select statement")

    #Define the grammar

    selectStatement << (select + 
                        ('*' | columns).setResultsName('Columns') +
                        _from +
                        tables.setResultsName ('Tables') +
                        Optional (where + Group (whereExpr), '').setResultsName('where').setDebug(False) +
                        Each ([Optional (groupby + columns ('groupby'), '').setDebug(False),
                                Optional (orderby + columns ('orderby'),'').setDebug(False)
                            ]) +
                        ';'
                    
                    )

    selectStatement.ignore(sqlComment)

    try :
        tokens = selectStatement.parseString(request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseInsertInto (request) :

    keywords = ["insert", "into", "values"]
    [insert , into , values] = [ CaselessKeyword (word) for word in keywords ]

    insertIntoStatement = Forward().setName("Insert statement")

    table_name = Word (alphas,alphanums)
    column = Word (alphas,alphanums)
    insert_columns = Group (delimitedList (column))
    column_value = Word (alphas,alphanums) | Word (nums)
    insert_values = Group (delimitedList (column_value))

    #Define the grammar 

    insertIntoStatement << ( insert +
                            into +
                            table_name.setResultsName('Table') + 
                            Optional ( '(' + insert_columns.setResultsName('Columns') + ')') +
                            values + 
                            '(' +
                            insert_values.setResultsName('Values') +
                            ')'
                        )

    insertIntoStatement.ignore(sqlComment)

    try :
        tokens = insertIntoStatement.parseString(request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseCreateUser (request) :

    createUserKeywords = ["create", "user", '_if', "_not", "exists", "identified", "by"]
    [create, user, _if, _not, exists, identified, by] = [ CaselessKeyword (word) for word in createUserKeywords]

    createUserStatement = Forward().setName('Create user statement')

    user_name = Word (alphas, alphanums)
    password = Word (alphas, alphanums)

    createUserStatement << ( create +
                            user + 
                            Optional (_if + _not + exists) +
                            user_name.setResultsName('Username') +
                            identified +
                            by +
                            password.setResultsName('Password') +
                            ';'

                        )

    createUserStatement.ignore(sqlComment)

    try :
        tokens = createUserStatement.parseString (request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseUseDatabase (request) :

    useDatabaseKeyword = "use"
    use = CaselessKeyword (useDatabaseKeyword)

    useDatabaseStatement = Forward().setName ('Use database')

    database_name = Word (alphas, alphanums)

    useDatabaseStatement << ( use +
                                database_name.setResultsName('Database') +
                                ';'
                            )

    useDatabaseStatement.ignore(sqlComment)

    try :
        tokens = useDatabaseStatement.parseString (request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

def parseDropDatabase(request) :

    dropDatabaseKeywords = ["drop", "database"]
    [drop, database] = [ CaselessKeyword (word) for word in dropDatabaseKeywords]

    dropDatabaseStatement = Forward().setName ('Drop database')

    database_name = Word (alphas, alphanums)

    dropDatabaseStatement << ( drop +
                                database +
                                database_name.setResultsName('Database') +
                                ';'
                            )

    dropDatabaseStatement.ignore(sqlComment)

    try :
        tokens = dropDatabaseStatement.parseString (request)
        return tokens
    except ParseException as err:
        print (" "*err.loc + err.msg)
        print(err)
    print()

