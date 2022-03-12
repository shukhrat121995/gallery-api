package com.starwars.api.tests;

import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;

public class AuthenticationTests extends TestInit {
    @Test(enabled = false) //TODO: not implemented yet
    public void verifyAuthTest() {
        given()
                .when()
                .get(HOST + "/api/auth")
                .then()
                .assertThat()
                .statusCode(200)
                .log().all();
    }
}
