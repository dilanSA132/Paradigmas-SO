module com.mycompany.so.paradigmas {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.base;

    opens com.mycompany.so.paradigmas to javafx.fxml;
    exports com.mycompany.so.paradigmas;
}
