package com.healthapp.clientmobile.domain.user;

public class User {
    private String firstName;
    private String lastName;
    private String email;
    private String password;
    private String birthDate;
    private double height;
    private double weight;
    private String gender;
    private double activityMultiplier;

    public User(String firstName, String lastName, String email, String password, String birthDate, double height, double weight, String gender, double activityMultiplier) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.birthDate = birthDate;
        this.height = height;
        this.weight = weight;
        this.gender = gender;
        this.activityMultiplier = activityMultiplier;
    }

    public User(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getBirthDate() {
        return birthDate;
    }

    public void setBirthDate(String birthDate) {
        this.birthDate = birthDate;
    }

    public double getHeight() {
        return height;
    }

    public void setHeight(double height) {
        this.height = height;
    }

    public double getWeight() {
        return weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public double getActivityMultiplier() {
        return activityMultiplier;
    }

    public void setActivityMultiplier(double activityMultiplier) {
        this.activityMultiplier = activityMultiplier;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }
}
