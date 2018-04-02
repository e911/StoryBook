from numpy import *
from scipy.optimize import minimize
from json import loads


def matrixize(userrating):
    items, users = [], []
    for k, v in userrating.items():
        if k not in users:
            users.append(k)
        for bk, rat in v.items():
            if bk not in items:
                items.append(bk)
    items.sort(), users.sort()
    Y = zeros((len(items), len(users)))
    R = copy(Y)
    i, j = 0, 0
    for i in range(len(items)):
        for j in range(len(users)):
            temp = userrating[users[j]]
            a = temp.get(items[i], None)
            if a:
                Y[i, j], R[i, j] = a, 1
    return Y, R, items, users


def normalizeRatings(Y, R):
    m, n = shape(Y)
    Ymean = zeros(m)
    Ynorm = zeros(shape(Y))
    for i in range(m):
        idx = where(R[i, :] == 1)
        Ymean[i] = mean(Y[i, idx])
        Ynorm[i, idx] = Y[i, idx] - Ymean[i]

    return Ynorm, Ymean


def serialize(*args):
    return hstack(a.ravel('F') for a in args)


def cofiCostFunc(params, Y, R, num_users, num_movies, num_features, lambda_):
    X = reshape(params[:num_movies * num_features],
                (num_movies, num_features), order='F')
    Theta = reshape(params[num_movies * num_features:],
                    (num_users, num_features), order='F')

    J = 0
    X_grad = zeros(shape(X))
    Theta_grad = zeros(shape(Theta))

    J_temp = (dot(X, Theta.T) - Y)**2
    J = (sum(J_temp[R == 1]) + lambda_ *
         sum(sum(Theta**2)) + lambda_ * sum(sum(X**2))) / 2

    X_grad = dot(((dot(X, Theta.T) - Y) * R), Theta) + lambda_ * X
    Theta_grad = dot(((dot(X, Theta.T) - Y) * R).T, X) + lambda_ * Theta

    grad = hstack((X_grad.ravel('F'), Theta_grad.ravel('F')))
    return J, grad


def recommend_gradient(username, data):
    ratings = loads(data.data)
    # ratings = {
    #     "Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
    #                  "Norah Jones": 4.5, "Phoenix": 5.0,
    #                  "Slightly Stoopid": 1.5,
    #                  "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #     "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5,
    #              "Deadmaus": 4.0, "Phoenix": 2.0,
    #              "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
    #     "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
    #              "Deadmaus": 1.0, "Norah Jones": 3.0,
    #              "Phoenix": 5, "Slightly Stoopid": 1.0},
    #     "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
    #             "Deadmaus": 4.5, "Phoenix": 3.0,
    #             "Slightly Stoopid": 4.5, "The Strokes": 4.0,
    #             "Vampire Weekend": 2.0},
    #     "Hailey": {"Broken Bells": 4.0, "Deadmaus": 1.0,
    #                "Norah Jones": 4.0, "The Strokes": 4.0,
    #                "Vampire Weekend": 1.0},
    #     "Jordyn": {"Broken Bells": 4.5, "Deadmaus": 4.0, "Norah Jones": 5.0,
    #                "Phoenix": 5.0, "Slightly Stoopid": 4.5,
    #                "The Strokes": 4.0, "Vampire Weekend": 4.0},
    #     "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
    #             "Norah Jones": 3.0, "Phoenix": 5.0,
    #             "Slightly Stoopid": 4.0, "The Strokes": 5.0},
    #     "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
    #                  "Phoenix": 4.0, "Slightly Stoopid": 2.5,
    #                  "The Strokes": 3.0}
    # }

    Y, R, stories, users = matrixize(ratings)

    num_users = size(Y, 1)
    num_movies = size(Y, 0)
    num_features = 10

    X = random.randn(num_movies, num_features)
    Theta = random.randn(num_users, num_features)

    initial_parameters = serialize(X, Theta)

    lambda_ = 10
    extra_args = (Y, R, num_users, num_movies, num_features, lambda_)

    res = minimize(cofiCostFunc, initial_parameters, extra_args, method='CG',
                   jac=True, options={'maxiter': 100})
    theta = res.x

    X = reshape(theta[:num_movies * num_features],
                (num_movies, num_features), order='F')
    Theta = reshape(theta[num_movies * num_features:],
                    (num_users, num_features), order='F')

    p = dot(X, Theta.T)
    id = users.index(username)
    return p[:, id].tolist(), stories


def pearsonVectorize(user1, user2, data):
    Y, R, stories, users = matrixize(data)
    i, j = users.index(user1), users.index(user2)
    X, Y = Y[:, i] * R[:, j].T, Y[:, j] * R[:, i].T
    Sx = sum(X)
    Sy = sum(Y)
    Sxy = sum(X * Y)
    Sxx = sum(X ** 2)
    Syy = sum(Y ** 2)
    condition = not_equal(X, 0)
    n = len(extract(condition, X))
    if n == 0:
        return 0
    denominator = sqrt(Sxx - (Sx**2) / n) * sqrt(Syy - (Sy**2) / n)
    if denominator == 0:
        return 0
    else:
        return -(Sxy - (Sx * Sy) / n) / denominator


def magnitudeVectorize(user, users, Y):
    i = users.index(user)
    return sqrt(sum(Y[:, i]**2))


def cosineVectorize(user1, user2, data):
    Y, R, stories, users = matrixize(data)
    i, j = users.index(user1), users.index(user2)
    x, y = Y[:, i] * R[:, j].T, Y[:, j] * R[:, i].T
    Sxx = magnitudeVectorize(user1, users, Y)
    Syy = magnitudeVectorize(user2, users, Y)
    Sxy = sum(x * y)
    if Sxx == 0 or Syy == 0:
        return 0
    else:
        return Sxy / (Sxx * Syy)


def computeNeighbour(username, data, func):
    distances = []
    for user in data:
        if user != username:
            distance = func(username, user, data)
            distances.append((distance, user))
    distances.sort()
    return distances


def recommend_knn(username, data, function='Cosine'):
    if function == 'Pearson':
        func = pearsonVectorize
    else:
        func = cosineVectorize
    rating = loads(data.data)
    # rating = {
    #     "Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
    #                  "Norah Jones": 4.5, "Phoenix": 5.0,
    #                  "Slightly Stoopid": 1.5,
    #                  "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #     "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5,
    #              "Deadmaus": 4.0, "Phoenix": 2.0,
    #              "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
    #     "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
    #              "Deadmaus": 1.0, "Norah Jones": 3.0,
    #              "Phoenix": 5, "Slightly Stoopid": 1.0},
    #     "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
    #             "Deadmaus": 4.5, "Phoenix": 3.0,
    #             "Slightly Stoopid": 4.5, "The Strokes": 4.0,
    #             "Vampire Weekend": 2.0},
    #     "Hailey": {"Broken Bells": 4.0, "Deadmaus": 1.0,
    #                "Norah Jones": 4.0, "The Strokes": 4.0,
    #                "Vampire Weekend": 1.0},
    #     "Jordyn": {"Broken Bells": 4.5, "Deadmaus": 4.0, "Norah Jones": 5.0,
    #                "Phoenix": 5.0, "Slightly Stoopid": 4.5,
    #                "The Strokes": 4.0, "Vampire Weekend": 4.0},
    #     "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
    #             "Norah Jones": 3.0, "Phoenix": 5.0,
    #             "Slightly Stoopid": 4.0, "The Strokes": 5.0},
    #     "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
    #                  "Phoenix": 4.0, "Slightly Stoopid": 2.5,
    #                  "The Strokes": 3.0}
    # }
    nearest = computeNeighbour(username, rating, func)[0][1]
    recommendations = []

    neighbourRating = rating[nearest]
    userRating = rating[username]

    for story in neighbourRating:
        if story not in userRating:
            recommendations.append((story, neighbourRating[story]))
    return sorted(recommendations, key=lambda storyTuple: storyTuple[1], reverse=True)
