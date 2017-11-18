import random
from pico2d import *
import game_framework
import start_state

# 상태들은 게임 칩이라고 생각하고 게임 프레임워크는 고전게임기 라고 생각하면 편하다.
# 게임기는 run함수로 상태라는 칩을 꼽고 무한히 반복한다.
# 그 칩에서의 고유 사용자입력/업데이트/그리기를 처리한다.

# 모든 칩은 enter/exit/update/draw/resume/pause/handleevents를 가진다. 이는 게임기에서 동작하기위한 필수요소인 함수들이다.
# 즉 어떤 칩(상태들)을 구현하기위한 방법은 저 7가지만 구현만 잘해두면 어느정도 돌아간다.
# enter는 해당 상태로 들어갈때 해야하는 일들을 한다. 가장 대표적인게 초기화다.
# exit는 해당 칩을 제거할때 해야하는 일들이다. 보통 enter에서 초기화하며 생성한 리소스들을 제거한다.
# update는 게임의 꽃으로 모든 게임오브젝트의 고유의 update함수를 호출시키며 갱신시킨다.
# draw는 화면에 실제적으로 그리는 것이며, 기존에 그린것을 지우고 그려야 할것을 그리고, 최종적으로 플리핑한다.
# resume는 puase를 풀며 이전 상태로 돌아간다.
# pause는 잠시 상태의 처리를 멈춘다.
# handleevents 또한 게임의 꽃으로 사용자가 게임세상과 소통하도록 하는 녀석이다. 예를들어 시작 상태의 경우 스페이스바를 눌러서
# 게임을 진행하거나 esc를 눌러서 종료할수 있도록한다.


game_framework.run(start_state)
