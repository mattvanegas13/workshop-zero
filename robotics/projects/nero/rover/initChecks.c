int checkCamera(){
    return 0;
}

int checkMotors(){
    return 0 ;
}

int checkServerStream(){
    return 0;
}

// Collect all the checks in a systemchecks structs as a collection of function pointers 
typedef struct {
    int (*checkCamera)();
    int (*checkMotors)();
    int *checkServerStream;
} SystemChecks;
