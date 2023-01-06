# rate_funcs
def constant(current_frame, total_frames):
    return 1


def linear_increase(current_frame, total_frames):
    return current_frame / total_frames * 2


def linear_decrease(current_frame, total_frames):
    return (1 - current_frame / total_frames) * 2


def there_and_back(current_frame, total_frames):
    if current_frame / total_frames < 0.5:
        return linear_increase(current_frame, total_frames)

    if current_frame / total_frames >= 0.5:
        return linear_decrease(current_frame, total_frames)


def pack_rgba(red: int, green: int, blue: int, alpha: int):
    return (red << 24) | (green << 16) | (blue << 8) | alpha
