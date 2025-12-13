const express = require('express');
const bcrypt = require('bcrypt');

const User = require('../models/user');

const router = express.Router();

router.get('/sign-up', (req, res) => {
  res.render('auth/sign-up.ejs');
});

router.get('/sign-in', (req, res) => {
  res.render('auth/sign-in.ejs');
});

router.post('/sign-up', async (req, res) => {
  const userInDatabase = await User.findOne({ username: req.body.username });

  if (userInDatabase) {
    return res.send('Username or Password is invalid');
  }

  if (req.body.password !== req.body.confirmPassword) {
    return res.send('Password and Confirm Password must match');
  }

  const hashedPassword = bcrypt.hashSync(req.body.password, 10);
  req.body.password = hashedPassword;

  const newUser = await User.create(req.body);

  req.session.user = {
    username: newUser.username,
    _id: newUser._id
  };

  req.session.save(() => {
    res.redirect("/");
  });
});

router.post('/sign-in', async (req, res) => {
  const userInDatabase = await User.findOne({ username: req.body.username });

  if (!userInDatabase) {
    return res.send('Username or Password is invalid');
  }

  const validPassword = bcrypt.compareSync(req.body.password, userInDatabase.password);

  if (!validPassword) {
    return res.send('Username or Password is invalid');
  }

  req.session.user = {
    username: userInDatabase.username,
    _id: userInDatabase._id,
  };

  req.session.save(() => {
    res.redirect('/');
  });
});

router.get("/sign-out", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/");
  });
});



module.exports = router;
