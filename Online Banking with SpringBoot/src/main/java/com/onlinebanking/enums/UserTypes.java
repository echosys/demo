package com.onlinebanking.enums;

public enum UserTypes {

    ADMIN(0), TIER_1(1), TIER_2(2), CUSTOMER(3), MERCHANT(4);

    private final int value;

    UserTypes(int type){
        this.value = type;
    }

    public int getType(){
         return this.value;
    }

    public static UserTypes fromInt(int in){
        switch(in) {
            case 0:
                return ADMIN;
            case 1:
                return TIER_1;
            case 2:
                return TIER_2;
            case 3:
                return CUSTOMER;
            case 4:
                return MERCHANT;
        }
        return null;
    }

}