-- Add job and message tables
-- Migration: 20250714_add_job_and_message_tables.sql

-- Create job table
CREATE TABLE IF NOT EXISTS `job` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `company` VARCHAR(200) NOT NULL,
    `location` VARCHAR(200) NOT NULL,
    `category` VARCHAR(100) NOT NULL,
    `description` TEXT NOT NULL,
    `requirements` TEXT,
    `salary_min` INT,
    `salary_max` INT,
    `employment_type` VARCHAR(50),
    `experience_level` VARCHAR(50),
    `status` VARCHAR(20) DEFAULT 'active',
    `posted_by` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`posted_by`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    INDEX `idx_job_status` (`status`),
    INDEX `idx_job_category` (`category`),
    INDEX `idx_job_location` (`location`),
    INDEX `idx_job_posted_by` (`posted_by`),
    INDEX `idx_job_created_at` (`created_at`)
);

-- Create job_application table
CREATE TABLE IF NOT EXISTS `job_application` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `job_id` INT NOT NULL,
    `applicant_id` INT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'pending',
    `cover_letter` TEXT,
    `resume_url` VARCHAR(500),
    `applied_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `reviewed_at` DATETIME,
    FOREIGN KEY (`job_id`) REFERENCES `job`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`applicant_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    INDEX `idx_job_application_job_id` (`job_id`),
    INDEX `idx_job_application_applicant_id` (`applicant_id`),
    INDEX `idx_job_application_status` (`status`),
    UNIQUE KEY `unique_job_applicant` (`job_id`, `applicant_id`)
);

-- Create conversation table
CREATE TABLE IF NOT EXISTS `conversation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user1_id` INT NOT NULL,
    `user2_id` INT NOT NULL,
    `last_message` TEXT,
    `last_message_time` DATETIME,
    `unread_count` INT DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user1_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user2_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    INDEX `idx_conversation_user1_id` (`user1_id`),
    INDEX `idx_conversation_user2_id` (`user2_id`),
    INDEX `idx_conversation_last_message_time` (`last_message_time`),
    UNIQUE KEY `unique_conversation_users` (`user1_id`, `user2_id`)
);

-- Create message table
CREATE TABLE IF NOT EXISTS `message` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `conversation_id` INT NOT NULL,
    `sender_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `is_read` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`conversation_id`) REFERENCES `conversation`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sender_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    INDEX `idx_message_conversation_id` (`conversation_id`),
    INDEX `idx_message_sender_id` (`sender_id`),
    INDEX `idx_message_created_at` (`created_at`)
); 