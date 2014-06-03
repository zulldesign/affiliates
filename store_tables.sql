-- phpMyAdmin SQL Dump
-- version 2.11.9.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 09, 2010 at 01:01 AM
-- Server version: 5.0.83
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `thestore_tscdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `store_cats_tab`
--

CREATE TABLE IF NOT EXISTS `store_cats_tab` (
  `mem_id` int(11) NOT NULL default '0',
  `category_name` varchar(50) NOT NULL default '',
  `category_title` text,
  `category_desc` text,
  `category_key` text,
  PRIMARY KEY  (`category_name`,`mem_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `store_info_tab`
--

CREATE TABLE IF NOT EXISTS `store_info_tab` (
  `mem_id` int(11) NOT NULL auto_increment,
  `password` varchar(10) NOT NULL default '',
  `contact_email` varchar(250) NOT NULL default '',
  `paypal_email` varchar(250) default NULL,
  `mem_status` varchar(10) NOT NULL default 'pending',
  `conf_code` varchar(10) NOT NULL,
  `addedon` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `store_title` varchar(250) default NULL,
  `short_desc` text,
  `contact` text,
  `about` text,
  `welcome_note` text,
  `welcome_img` text,
  `store_currency` varchar(5) NOT NULL default '',
  `store_category` varchar(250) default NULL,
  `image_center` text,
  `template` varchar(10) default NULL,
  `inv_limit` int(10) NOT NULL default '20',
  `store_thankyou` text,
  UNIQUE KEY `username` (`mem_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

-- --------------------------------------------------------

--
-- Table structure for table `store_items_tab`
--

CREATE TABLE IF NOT EXISTS `store_items_tab` (
  `mem_id` varchar(10) NOT NULL default '',
  `category_name` varchar(50) NOT NULL default '',
  `item_type` varchar(10) default NULL,
  `item_id` varchar(20) NOT NULL default '',
  `item_title` text NOT NULL,
  `item_qty` int(11) NOT NULL default '0',
  `item_price` varchar(10) NOT NULL default '',
  `item_shipping` varchar(100) default NULL,
  `item_image` text,
  `item_details` text,
  `item_dwld_url` text,
  `item_category` varchar(20) NOT NULL default 'Physical goods',
  PRIMARY KEY  (`mem_id`,`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
