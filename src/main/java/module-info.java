module com.mycompany.paradigmas_so {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.base;

    opens com.mycompany.paradigmas_so to javafx.fxml;
    exports com.mycompany.paradigmas_so;
}
