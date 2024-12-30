package com.mc.mobileapp.daos

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.mc.mobileapp.domains.User

@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)

    @Query("SELECT * FROM users WHERE email = :email AND password = :password")
    suspend fun findUserEmailPassword(email: String, password: String): User?

    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<User>

    @Query("SELECT id FROM users WHERE email = :email LIMIT 1")
    suspend fun getUserId(email: String): Int?

    @Query("SELECT trustScore FROM users WHERE email = :email LIMIT 1")
    suspend fun getUserTrustScore(email: String): Int?

    @Query("UPDATE users SET trustScore = :trustScore WHERE id = :id")
    suspend fun updateTrustScore(id: Int, trustScore: Int)

    @Delete
    suspend fun deleteUser(user: User)
}
