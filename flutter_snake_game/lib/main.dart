import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';

void main() => runApp(const SnakeGame());

class SnakeGame extends StatelessWidget {
  const SnakeGame({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: GameScreen(),
    );
  }
}

class GameScreen extends StatefulWidget {
  @override
  _GameScreenState createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  static const int gridSize = 20;
  static const int numberOfSquares = gridSize * gridSize;

  List<int> snakePosition = [0, 1, 2];
  int foodPosition = Random().nextInt(numberOfSquares);

  String direction = 'right';
  late Timer timer;
  int lives = 3;

  @override
  void initState() {
    super.initState();
    startGame();
  }

  void startGame() {
    setState(() {
      snakePosition = [0, 1, 2];
      foodPosition = Random().nextInt(numberOfSquares);
      direction = 'right';
      lives = 3;
      timer = Timer.periodic(Duration(milliseconds: 300), (timer) {
        updateSnake();
      });
    });
  }

  void updateSnake() {
    setState(() {
      int nextPosition;

      // Calcula la próxima posición según la dirección
      switch (direction) {
        case 'up':
          nextPosition = snakePosition.last - gridSize;
          break;
        case 'down':
          nextPosition = snakePosition.last + gridSize;
          break;
        case 'left':
          nextPosition = snakePosition.last - 1;
          break;
        case 'right':
          nextPosition = snakePosition.last + 1;
          break;
        default:
          return;
      }

      // Detecta colisión con las paredes
      if (isWallCollision(nextPosition)) {
        handleCollision();
        return;
      }

      // Agrega la nueva posición a la serpiente
      snakePosition.add(nextPosition);

      // Si come la comida
      if (snakePosition.last == foodPosition) {
        foodPosition = Random().nextInt(numberOfSquares);
      } else {
        snakePosition.removeAt(0);
      }

      // Detecta colisión consigo misma
      if (checkSelfCollision()) {
        handleCollision();
      }
    });
  }

  bool isWallCollision(int nextPosition) {
    // Colisión con la parte superior o inferior
    if (nextPosition < 0 || nextPosition >= numberOfSquares) {
      return true;
    }

    // Colisión con la parte izquierda o derecha
    if (direction == 'left' && nextPosition % gridSize == gridSize - 1) {
      return true;
    }
    if (direction == 'right' && nextPosition % gridSize == 0) {
      return true;
    }

    return false;
  }

  bool checkSelfCollision() {
    List<int> body = List.from(snakePosition);
    body.removeLast();
    return body.contains(snakePosition.last);
  }

  void handleCollision() {
    if (lives > 1) {
      // Reduce una vida y reinicia la posición de la serpiente
      setState(() {
        lives--;
        snakePosition = [0, 1, 2];
        direction = 'right';
      });
    } else {
      // Si no hay más vidas, termina el juego
      timer.cancel();
      showGameOverDialog();
    }
  }

  void showGameOverDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Game Over'),
          content: Text('Your score: ${snakePosition.length - 3}'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                startGame();
              },
              child: Text('Play Again'),
            ),
          ],
        );
      },
    );
  }

  void changeDirection(String newDirection) {
    if ((direction == 'up' && newDirection != 'down') ||
        (direction == 'down' && newDirection != 'up') ||
        (direction == 'left' && newDirection != 'right') ||
        (direction == 'right' && newDirection != 'left')) {
      direction = newDirection;
    }
  }

  Widget buildGameBoard() {
    List<Widget> squares = List.generate(numberOfSquares, (index) {
      bool isSnake = snakePosition.contains(index);
      bool isFood = index == foodPosition;

      return Container(
        margin: EdgeInsets.all(1),
        decoration: BoxDecoration(
          color: isSnake
              ? Colors.green
              : isFood
                  ? Colors.red
                  : Colors.grey[900],
          borderRadius: BorderRadius.circular(4),
        ),
      );
    });

    return GridView.builder(
      itemCount: numberOfSquares,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: gridSize,
      ),
      itemBuilder: (context, index) => squares[index],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text('Snake Game - Lives: $lives'),
        centerTitle: true,
        backgroundColor: Colors.green,
      ),
      body: Column(
        children: [
          Expanded(
            child: buildGameBoard(),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () => changeDirection('left'),
                  child: Icon(Icons.arrow_left),
                ),
                Column(
                  children: [
                    ElevatedButton(
                      onPressed: () => changeDirection('up'),
                      child: Icon(Icons.arrow_drop_up),
                    ),
                    SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: () => changeDirection('down'),
                      child: Icon(Icons.arrow_drop_down),
                    ),
                  ],
                ),
                ElevatedButton(
                  onPressed: () => changeDirection('right'),
                  child: Icon(Icons.arrow_right),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
