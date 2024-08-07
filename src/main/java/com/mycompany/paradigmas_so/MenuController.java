/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/javafx/FXMLController.java to edit this template
 */
package com.mycompany.paradigmas_so;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;

import javafx.scene.control.Button;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.VBox;
/**
 * FXML Controller class
 *
 * @author Dilan
 */
public class MenuController implements Initializable {


    @FXML
    private ImageView imageRoot;
    @FXML
    private Button CopilerView;
    @FXML
    private Button GuideView;
    @FXML
    private Button AboutView;
    @FXML
    private AnchorPane root;
    /**
     * Initializes the controller class.
     */
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        
           imageRoot.fitHeightProperty().bind(root.heightProperty());
        imageRoot.fitWidthProperty().bind(root.widthProperty());      
       
        

    }    
    
}
