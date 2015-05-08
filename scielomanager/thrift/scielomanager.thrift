exception ServerError {
    1: string message;
}

exception DuplicationError {
    1: string message;
}

exception ValueError {
    1: string message;
}

service JournalManagerServices {
    string addArticle(1:string xml_string, 2:bool raw) throws (
        1:DuplicationError dup_err, 2:ValueError val_err, 3:ServerError srv_err);
}

