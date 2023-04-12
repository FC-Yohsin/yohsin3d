from yohsin3d.movement import Movement, MovementPhase
from yohsin3d import Joint


def create_wave_skill():
    def move_arm_phase1():
        phase = MovementPhase(0.5)
        phase.add(Joint.RA1, -120, 15.0)
        phase.add(Joint.RA2, -95, 15.0)
        phase.add(Joint.RA3, -120, 15.0)
        phase.add(Joint.RA4, 0, 15.0)
        return phase
    
    def move_arm_phase2():
        phase = MovementPhase(0.5)
        phase.add(Joint.RA1, -120, 15.0)
        phase.add(Joint.RA2, -95, 15.0)
        phase.add(Joint.RA3, -120, 15.0)
        phase.add(Joint.RA4, 90, 15.0)
        return phase

    def get_phases():
        return [move_arm_phase1(), move_arm_phase2()]
    
    wave_skill = Movement()
    wave_skill.add_phases(get_phases())
    return wave_skill



wave_skill = create_wave_skill()
